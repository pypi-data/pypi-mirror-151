from trame.app import get_server, jupyter
from . import engine, ui, assets
import logging

def show(input, output, auto_delete=True, name="default", **kwargs):
    engine_logger = logging.getLogger("trame_sandtank.app.engine")
    engine_logger.setLevel(logging.WARNING)

    server = get_server(name)
    assets.initialize(server)
    engine.initialize(server, input, output, auto_delete)
    ui.initialize(server)
    jupyter.show(server, **kwargs)