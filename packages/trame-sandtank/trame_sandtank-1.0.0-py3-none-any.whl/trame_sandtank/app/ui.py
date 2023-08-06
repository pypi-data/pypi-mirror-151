from trame.ui.vuetify import VAppLayout
from trame.widgets import html, vuetify
from trame_sandtank.html import Visualization, MaterialEditor

from pathlib import Path

STYLE_COMPACT = {"dense": True, "hide_details": True}

def initialize(server):
    server.state.trame__title = "ParFlow Sandtank"
    ctrl = server.controller

    def open_help():
        server.js_call(ref="viz", method="openHelp")

    with VAppLayout(server) as layout:
        with layout.root:
            # --- App bar
            with vuetify.VAppBar(app=True, flat=True, style="z-index: 100;"):
                with vuetify.VBtn(
                    icon=True, click="$vuetify.theme.dark = !$vuetify.theme.dark"
                ):
                    vuetify.VIcon("mdi-water", color="blue")
                vuetify.VToolbarTitle("ParFlow sandtank", classes="pl-0")
                vuetify.VSpacer()
                vuetify.VSelect(
                    v_model=("config_lake", 1),
                    items=(
                        "config_lake_modes",
                        [
                            {"text": "Lake", "value": 1},
                            {"text": "River", "value": 0},
                        ],
                    ),
                    **STYLE_COMPACT,
                    classes="mx-4",
                    style="max-width: 100px",
                )
                vuetify.VSlider(
                    v_if=("domain?.features?.includes('recharge')",),
                    v_model=("config_recharge", 0),
                    min=0,
                    max=5,
                    step=0.1,
                    label="Recharge",
                    **STYLE_COMPACT,
                    classes="mx-4",
                    thumb_label=True,
                    thumb_size=15,
                )
                vuetify.VSpacer()
                with vuetify.VRow(classes="mr-4 text-right", style="max-width: 54px;"):
                    vuetify.VIcon("mdi-clock-outline")
                    html.Div("{{ parflow_timestamp }}", style="min-width: 30px;")
                with vuetify.VBtn(
                    click=ctrl.parflow_run,
                    outlined=True,
                    disabled=("parflow_running", False),
                    classes="ml-2",
                ) as btn:
                    vuetify.VProgressCircular(
                        v_show=("parflow_running",),
                        size=20,
                        width=2,
                        indeterminate=True,
                        color="primary",
                        classes="mr-2",
                        style="width: 30px;",
                    )
                    vuetify.VIcon(
                        "mdi-autorenew",
                        v_show=("!parflow_running",),
                        classes="mr-2",
                        style="width: 30px",
                    )
                    btn.add_child("Run")
                vuetify.VBtn(
                    "Reset",
                    click=ctrl.parflow_reset,
                    outlined=True,
                    disabled=("parflow_running", False),
                    classes="ml-2",
                )
                with vuetify.VTooltip(bottom=True) as tt:
                    with vuetify.Template(v_slot_activator="{ on }"):
                        with vuetify.VBtn(
                            v_on=("on",),
                            icon=True,
                            classes="ml-2",
                            small=True,
                            click=("ui_show_about = !ui_show_about"),
                            __properties=["v_on"],
                        ):
                            vuetify.VIcon("mdi-help-circle-outline")
                    html.Span(v_html=("computed_data_tooltip", ""))

                vuetify.VProgressLinear(
                    active=("trame__busy",),
                    absolute=True,
                    bottom=True,
                    color="light-blue",
                    height=4,
                    indeterminate=True,
                )

            # --- App content
            with vuetify.VMain():
                with vuetify.VContainer(fluid=True, classes="fill-height"):
                    with vuetify.VCol():
                        Visualization(
                            ref="viz",
                            domain=("domain", None),
                            water_height_left=("config_height_left",),
                            water_height_right=("config_height_right",),
                            indicator=("indicator", None),
                            saturation=("saturation", None),
                            pressures=("pressures", None),
                            permeability=("config_k", None),
                            wells=("config_wells", None),
                            mask=("mask", None),
                            concentration=("concentration", None),
                            show_opacity_sliders=("ui_show_advanced", False),
                            # events
                            UpdateWells="config_wells = $event",
                            UpdateLeftHeight="config_height_left = $event",
                            UpdateRightHeight="config_height_right = $event",
                            Exit=ctrl.on_exit,
                        )
                        with vuetify.VBtn(
                            click="ui_show_advanced = !ui_show_advanced",
                            absolute=True,
                            left=True,
                            icon=True,
                            style="top: 2px; left: 2px;",
                        ):
                            vuetify.VIcon("mdi-tune")
                        with vuetify.VBtn(
                            click=open_help,
                            absolute=True,
                            left=True,
                            icon=True,
                            style="top: 2px; left: 42px;",
                        ):
                            vuetify.VIcon("mdi-lifebuoy")
                        MaterialEditor(
                            v_show=("ui_show_advanced", False),
                            domain=("domain", None),
                            indicator=("indicator", None),
                            permeability=("config_k", None),
                            wells=("config_wells", None),
                            mask=("mask", None),
                            force_resize=("ui_show_advanced", False),
                            UpdateK="config_k = $event",
                        )
                        vuetify.VSpacer()

            # --- About dialog
            with vuetify.VDialog(
                v_model=("ui_show_about", False),
                max_width="50%",
            ):
                with vuetify.VCard():
                    with vuetify.VCardTitle(
                        classes="align-center d-flex justify-space-between"
                    ):
                        html.Div("HydroFrame Sandtank Educational Model")
                        with vuetify.VBtn(icon=True, click="ui_show_about = false"):
                            vuetify.VIcon("mdi-close")
                    vuetify.VDivider()
                    with vuetify.VCardText() as txt:
                        txt.add_child(
                            """
                            <p class="body-1 pt-4">
                              The ParFlow Sandtank model is a free tool that allows users to
                              interactively simulate and visualize groundwater movement through a
                              virtual slice of the subsurface. The  app is designed to teach hydrogeology
                              concepts. Users can adjust groundwater levels, change subsurface
                              properties, pump groundwater, add pollutants and watch the system respond
                              in real time.
                            </p>
                            <p class="body-1 pt-4">
                              The ParFlow Sandtank can be used as a stand-alone tool or as a supplement
                              to existing lessons that use physical sand tank models. Refer to the
                              <a href="https://www.hydroframe.org/sand-tank-user-manual">User Manual</a>
                              and <a href="https://www.hydroframe.org/lesson-plans">Lesson Plan Video</a>
                              For more information and check out the
                               <a href="https://www.hydroframe.org/groundwater-education-tools">HydroFrame Education</a>
                               page for additional groundwater education resources.
                            </p>
                            <p class="body-1 pt-4">
                              <a href="https://github.com/hydroframe/SandTank">ParFlow Sandtank</a>
                              is an open-source web application designed by the
                              <a href="https://www.hydroframe.org/"">HydroFrame Team</a> and developed by
                              <a href="https://www.kitware.com/">Kitware</a>
                              to support increased accessibility and usability of hydrology tools for
                              research and teaching. It uses
                              <a href="https://parflow.org/">ParFlow</a> for its simulation backend and
                              <a href="https://www.paraview.org">ParaView</a> for the data loading and
                              processing. The communication infrastructure relies on the
                              <a href="http://www.paraview.org/web/">ParaViewWeb</a> framework.
                            </p>
                            <p>
                              <b>Acknowledgment:</b> This material is based upon work supported by the
                              Department of Energy under Award Number(s) DE-SC0019609 - Cloud/Web-based
                              Advanced Modeling and Simulation Turnkey High-Performance Computing
                              Environment for Surface and Subsurface Science and the US National Science
                              Foundation Office of Advanced Cyberinfrastructure under Award number
                              OAC-1835855.
                            </p>
                        """
                        )
                        with html.Div(
                            classes="d-flex justify-center align-center flex-wrap px-2 rounded-lg",
                            style="background: white;",
                        ) as c:
                            c.add_child(
                                """
                                <img
                                    v-for="logo, idx in logos"
                                    :key="idx"
                                    :src="logo"
                                    style="height: 35px; margin: 10px 20px"
                                />
                            """
                            )
