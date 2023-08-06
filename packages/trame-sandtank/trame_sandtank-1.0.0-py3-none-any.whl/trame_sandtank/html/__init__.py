from trame_client.widgets.core import AbstractElement
from . import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class MaterialEditor(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__("material-editor", **kwargs)
        self._attr_names += [
            "domain",
            "indicator",
            "permeability",
            "mask",
            ("force_resize", "forceResize"),
            "palette",
        ]
        self._event_names += ["UpdateK"]


class Visualization(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__("visualization", **kwargs)
        self._attr_names += [
            "domain",
            ("water_height_left", "waterHeightLeft"),
            ("water_height_right", "waterHeightRight"),
            "indicator",
            "saturation",
            "permeability",
            "wells",
            "mask",
            "pressures",
            "concentration",
            ("slider_width", "sliderWidth"),
            ("control_offset", "controlOffset"),
            ("show_opacity_sliders", "showOpacitySliders"),
        ]
        self._event_names += [
            "input",
            "UpdateWells",
            "UpdateRightHeight",
            "UpdateLeftHeight",
            "UpdateScale",
            "Exit",
        ]
