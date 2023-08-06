import asyncio
import json
import multiprocessing
import numpy as np
import os
import shutil
import stat
import subprocess
import logging

from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

# ParFlow
from parflow.tools.io import read_pfb

# trame
from trame.app import asynchronous

# VTK
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkFiltersCore import vtkResampleToImage
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.web.utils import np_encode

SPAWN = multiprocessing.get_context("spawn")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# -------------------------------------------------------------------------------------------
# Data extractor
# -------------------------------------------------------------------------------------------
class DataExtractor:
    def __init__(self, server, domain, file_helper):
        self._state = server.state
        self._domain = domain
        self._files = file_helper
        self.reset()

    def reset(self):
        self.total_pumping = 0
        self.total_storage = 0
        self.pressures = {}
        self.flows = {}
        self.storages = {}

    def update_time(self, pf_time, eco_time):
        self._files.set_time(pf_time, eco_time)

    @property
    def is_ecoslim_ready(self):
        return self._files.has_next_eco_slim

    @property
    def is_parflow_ready(self):
        return self._files.has_next_parflow

    def process_pressure(self):
        press_array = read_pfb(self._files.pressure)
        press_array_1d = press_array.ravel()

        # Extract pressures
        pressures = {}
        for press in self._domain["pressures"]:
            key = press["name"]
            i, j, k = press["pressureCell"]
            value = press_array[k, j, i]
            pressures[key] = value

        # Extract flows
        flows = {}
        for flow in self._domain["flows"]:
            key = flow["name"]
            ratio = flow["ratio"]
            totalFlow = 0.0
            for cellId in flow["cells"]:
                p = press_array_1d[cellId]
                if p > 0.0:
                    totalFlow += ratio * (p ** (5.0 / 3.0))
            flows[key] = totalFlow

        # Extract storage
        storages = {}
        for storage in self._domain["storages"]:
            key = storage["name"]
            ratio = storage["ratio"]
            totalStorage = 0.0
            for cellId in storage["cells"]:
                p = press_array_1d[cellId]
                if p > 0.0:
                    totalStorage += ratio * p
            storages[key] = totalStorage

        # Save computed data
        self.pressures = pressures
        self.flows = flows
        self.storages = storages

    def process_saturation(self):
        saturation_array = read_pfb(self._files.saturation).ravel()
        out_sat = np.zeros((saturation_array.size), dtype=np.uint8)

        # Extract and publish saturation and total storage in the domain
        totalStorage = 0.0
        for i in range(saturation_array.size):
            value = saturation_array[i]
            if value >= 1.0:
                out_sat[i] = 255
            elif value < 0.0:
                out_sat[i] = 0
            else:
                out_sat[i] = int(value * 255)

            totalStorage += out_sat[i]

        self.total_storage += totalStorage * 0.3

        return np_encode(out_sat)

    def process_wells(self):
        array = read_pfb(self._files.well_forcing).ravel()
        pumping = 0.0
        for value in np.nditer(array):
            if value < 0:
                pumping -= value

        self.total_pumping += pumping

    def process_concentration(self):
        reader = vtkDataSetReader()
        reader.SetFileName(self._files.concentration)
        reader.Update()
        image_data = reader.GetOutput()

        if image_data:
            array = image_data.GetCellData().GetArray("Concentration")
            data_range = array.GetRange(0)
            return {
                "range": data_range,
                "array": np_encode(vtk_to_numpy(array)),
            }

    def process_indicator(self):
        indicator_array = read_pfb(self._files.indicator)
        return {
            "dimensions": list(indicator_array.shape),
            "array": np_encode(indicator_array, np.uint8),
        }

    def process_mask(self, scale=5):
        sampling = [v * scale if v > 1 else 1 for v in self._domain["dimensions"]]
        reader = vtkDataSetReader()
        reader.SetFileName(self._files.mask)
        image_filter = vtkResampleToImage()
        image_filter.UseInputBoundsOff()
        image_filter.SetSamplingBounds(self._domain["bounds"])
        image_filter.SetSamplingDimensions(sampling)
        image_filter.SetInputConnection(reader.GetOutputPort())
        image_filter.Update()
        mask = image_filter.GetOutput().GetPointData().GetArray("vtkValidPointMask")
        return {"array": np_encode(vtk_to_numpy(mask)), "scale": scale}

    @property
    def tooltip(self):
        lines = []

        # Unit extraction
        lake_unit = ""
        river_unit = ""
        for item in self._domain["storages"]:
            if item.get("name") == "lake":
                lake_unit = item.get("unit")
        for item in self._domain["flows"]:
            if item.get("name") == "river":
                river_unit = item.get("unit")

        # Lake / River info
        if self._state.config_lake:
            # Lake
            lines.append(f"Lake storage {self.storages.get('lake'):.4f} {lake_unit}")
        else:
            # River
            lines.append(f"River flow {self.flows.get('river'):.6f} {river_unit}")

        # Yield
        calc_yield = 0
        if "yield" in self._domain.get("features", []):
            calc_yield = (
                self.total_pumping
                * (self._state.config_water_use_efficiency * 0.004)
                * (self._state.config_irrigation_efficiency * 0.2)
            )
            lines.append(f"Yield {calc_yield:.4f} ton")

        # Revenu
        if "revenue" in self._domain.get("features", []):
            lines.append(f"Revenu ${calc_yield * 120:.2f}")

        # Total storage
        if "totalStorage" in self._domain.get("features", []):
            lines.append(f"Total Storage {self.total_storage:.1f} {lake_unit}")

        return "<br>".join(lines)

    def flush_state(self):
        with self._state:
            self._state.computed_data_tooltip = self.tooltip
            self._state.pressures = self.pressures



# -------------------------------------------------------------------------------------------
# ParFlow File Path helper
# -------------------------------------------------------------------------------------------
class ParFlowFileHelper:
    def __init__(self, name, working_dir):
        self._name = name
        self._working_dir = Path(working_dir)
        self._pf_t1 = "00000"
        self._pf_t2 = "00000"
        self._ec_t1 = "00000000"
        self._ec_t2 = "00000000"

    def set_time(self, pf_time, eco_slim_time):
        self._pf_t1 = str(pf_time + 1).zfill(5)
        self._pf_t2 = str(pf_time + 2).zfill(5)
        self._ec_t1 = str(eco_slim_time + 1).zfill(8)
        self._ec_t2 = str(eco_slim_time + 2).zfill(8)

    @property
    def well_forcing(self):
        return str(self._working_dir / "well_forcing.pfb")

    @property
    def saturation(self):
        return str(self._working_dir / f"{self._name}.out.satur.{self._pf_t1}.pfb")

    @property
    def pressure(self):
        return str(self._working_dir / f"{self._name}.out.press.{self._pf_t1}.pfb")

    @property
    def concentration(self):
        return str(self._working_dir / f"SLIM_SandTank_test_cgrid.{self._ec_t1}.vtk")

    @property
    def indicator(self):
        return str(self._working_dir / "SandTank_Indicator.pfb")

    @property
    def mask(self):
        return str(self._working_dir / "SandTank.vtk")

    @property
    def has_next_eco_slim(self):
        return (
            self._working_dir / f"SLIM_SandTank_test_cgrid.{self._ec_t2}.vtk"
        ).exists()

    @property
    def has_next_parflow(self):
        return (
            self._working_dir / f"{self._name}.out.satur.{self._pf_t2}.pfb"
        ).exists()


# -------------------------------------------------------------------------------------------
# Application engine
# -------------------------------------------------------------------------------------------
class SandtankEngine:
    def __init__(self, server, template_path, working_directory, delete_on_exit=False):
        self._server = server
        self._state = server.state
        self._monitoring = False
        self._delete_on_exit = delete_on_exit

        # Path handling
        self._input_base = Path(str(Path(template_path).resolve().absolute()))
        self._working_dir = Path(str(Path(working_directory).resolve().absolute()))
        self._name = self._working_dir.name
        self._file_helper = ParFlowFileHelper(self._name, self._working_dir)
        self._exec_script = str(
            (Path(__file__).parent / "assets/run.sh").resolve().absolute()
        )

        # Parflow executor pool
        self._pf_process_manager = multiprocessing.Manager()
        self._pf_pool = ProcessPoolExecutor(1, mp_context=SPAWN)

        # Fill state for client
        self._state.parflow_running = False
        self._state.parflow_timestamp = -1
        self._state.ecoslim_timestamp = -1

        with open(self._input_base / "domain.json", "r") as file:
            _domain = json.load(file)
            self._metadata = DataExtractor(self._server, _domain, self._file_helper)
            self._state.domain = _domain
            self._state.refresh_rate = _domain.get("server").get("refreshRate")

        # Fill working directory if missing
        if not self._working_dir.exists():
            self.reset()

        self._state.indicator = self._metadata.process_indicator()
        self._state.mask = self._metadata.process_mask(5)

        self.reset_run_config()

        # Bind methods to controller
        ctrl = server.controller
        ctrl.parflow_run = self.run
        ctrl.parflow_reset = self.reset
        ctrl.on_server_ready = self.load_existing_data
        ctrl.on_server_exited = self.exit


    def reset_run_config(self):
        _setup = self._state.domain.get("setup", {})
        _sim_length = _setup.get("simulationLength", 10)
        _reset = 0 if self.last_timestep > 0 else 1
        _hleft = _setup.get("hLeft", 30)
        _hright = _setup.get("hRight", 30)
        _ind = _setup.get("indicators", [])

        self._state.config_name = self._name
        self._state.config_run_length = _sim_length
        self._state.config_reset = _reset
        self._state.config_height_left = _hleft
        self._state.config_height_right = _hright
        self._state.config_recharge = 0
        self._state.config_water_use_efficiency = 1
        self._state.config_irrigation_efficiency = 1
        self._state.config_k = {item["key"]: item["value"] for item in _ind}
        self._state.config_wells = {i: 0 for i in range(1, 12)}

    def load_existing_data(self, **_):
        # Load any pre-existing data
        if not self._monitoring and self.last_timestep > 0:
            self._monitoring = True
            asynchronous.decorate_task(asyncio.create_task(self.monitor()))

    @property
    def last_timestep(self):
        count = 0
        filePattern = str(self._working_dir / f"{self._name}.out.satur.%s.pfb")
        while os.path.exists(filePattern % str(count + 1).zfill(5)):
            count += 1
        return count

    def reset(self):
        # Prepare working director
        if self._working_dir.exists():
            shutil.rmtree(self._working_dir)
        shutil.copytree(self._input_base, self._working_dir)

        # shell script to exec
        start_script = self._working_dir / "run.sh"
        shutil.copyfile(self._exec_script, start_script)
        file_perm = os.stat(start_script)
        os.chmod(start_script, file_perm.st_mode | stat.S_IEXEC)

        # Reset global variables
        self._monitoring = False
        self._metadata.reset()
        self._state.config_reset = 1
        self._state.parflow_timestamp = -1
        self._state.ecoslim_timestamp = -1

    def write_config(self, start_number):
        with open(self._working_dir / "config.tcl", "w") as f:
            # Global
            f.write("# Global settings\n")
            f.write(f"set reset          {self._state.config_reset}\n")
            f.write("\n")
            f.write(f"set StartNumber    {start_number}\n")
            f.write(f"set RunLength      {self._state.config_run_length}\n")
            f.write("\n")
            f.write(f"set hleft          {self._state.config_height_left}\n")
            f.write(f"set hright         {self._state.config_height_right}\n")
            f.write("\n")
            f.write(f"set lake           {self._state.config_lake}\n")
            f.write("\n")

            f.write(f"set recharge                   {self._state.config_recharge}\n")
            f.write(
                f"set waterUseEfficiency         {self._state.config_water_use_efficiency}\n"
            )
            f.write(
                f"set irrigationEfficiency       {self._state.config_irrigation_efficiency}\n"
            )
            f.write("\n")

            # Porosity
            f.write("\n# Update Porosity\n")
            for name, value in self._state.config_k.items():
                f.write(f"set k_{name}       {value}\n")

            # Wells
            f.write("\n# Update Wells\n")
            for key, value in self._state.config_wells.items():
                action = "Extraction" if value < 0 else "Injection"
                f.write(f"set well_{key}_action     {action}\n")
                f.write(f"set well_{key}_value      {abs(value)}\n")

    def run(self):
        if self._state.config_reset:
            self.reset()

        start_number = self.last_timestep
        if self._state.parflow_timestamp > start_number:
            self._state.parflow_timestamp = start_number
            self._state.ecoslim_timestamp = start_number

        # Update config.tcl
        self.write_config(start_number)

        # Asynchronously run parflow and monitor output
        self._state.parflow_running = True
        asynchronous.create_task(self.parflow_start())
        if not self._monitoring:
            self._monitoring = True
            asynchronous.create_task(self.monitor())

    async def parflow_start(self):
        loop = asyncio.get_event_loop()
        cmd = [f"{self._working_dir / 'run.sh'} {self._name}"]
        await loop.run_in_executor(
            self._pf_pool,
            partial(subprocess.run, cmd, shell=True, stdout=subprocess.DEVNULL),
        )
        # reset wells
        with self._state:
            self._state.config_reset = 0
            self._state.config_wells = {key: 0 for key in self._state.config_wells}
            self._state.parflow_running = False

    async def monitor(self):
        """Check parflow output files"""
        while self._monitoring:
            found_file = False
            self._metadata.update_time(
                self._state.parflow_timestamp,
                self._state.ecoslim_timestamp,
            )

            if self._metadata.is_ecoslim_ready:
                try:
                    with self._state:
                        self._state.concentration = self._metadata.process_concentration()
                        self._state.ecoslim_timestamp += 1

                    found_file = True
                except Exception as e:
                    logger.info(f"Error: EcoSLIM files {self._state.ecoslim_timestamp}", e)

            if self._metadata.is_parflow_ready:
                found_file = True
                try:
                    with self._state:
                        self._state.saturation = self._metadata.process_saturation()
                        self._metadata.process_pressure()
                        self._metadata.process_wells()
                        self._state.parflow_timestamp += 1
                except Exception as e:
                    logger.info(f"Error: ParFlow files {self._state.parflow_timestamp}", e)

            if found_file:
                # Update tooltip + pressures
                self._metadata.flush_state()

                # wait before looking for the next file
                await asyncio.sleep(self._state.refresh_rate)
            else:
                if self._state.parflow_running:
                    await asyncio.sleep(self._state.refresh_rate / 3.0)
                else:
                    self._monitoring = False

    def exit(self):
        """Web client exit page"""
        if self._working_dir.exists() and self._delete_on_exit:
            shutil.rmtree(self._working_dir)


# ---------------------------------------------------------
# Just to debug/validate update with nested variable
# ---------------------------------------------------------

# @state.change("config_irrigation_efficiency", "config_water_use_efficiency", "config_recharge", "config_k")
# def change_detected(config_irrigation_efficiency, config_water_use_efficiency, config_recharge, config_k, **kwargs):
#     print("Change detected")
#     print(f" - config_recharge: {config_recharge}")
#     print(f" - config_water_use_efficiency: {config_water_use_efficiency}")
#     print(f" - config_irrigation_efficiency: {config_irrigation_efficiency}")
#     print(f" - config_k: {config_k}")

# ---------------------------------------------------------
# Initialization helper
# ---------------------------------------------------------

def initialize(server, template_path, working_directory, delete_on_exit=False):
    return SandtankEngine(server, template_path, working_directory, delete_on_exit)
