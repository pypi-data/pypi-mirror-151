from trame.assets.local import LocalFileManager

ASSET_MANAGER = LocalFileManager(__file__)

# Logos
ASSET_MANAGER.url("logo_arizona", "logo-arizona.png")
ASSET_MANAGER.url("logo_igwmc", "logo-igwmc.png")
ASSET_MANAGER.url("logo_kitware", "logo-kitware.svg")
ASSET_MANAGER.url("logo_princeton", "PU-standard.png")
ASSET_MANAGER.url("logo_hmei", "HMEI-logo-light-bg.png")

# Favicon
ASSET_MANAGER.url("favicon", "favicon.png")

LOGOS = [
    ASSET_MANAGER.logo_kitware,
    ASSET_MANAGER.logo_arizona,
    ASSET_MANAGER.logo_igwmc,
    ASSET_MANAGER.logo_princeton,
    ASSET_MANAGER.logo_hmei,
]

def initialize(server):
    server.state.logos = LOGOS
    server.state.trame__favicon = ASSET_MANAGER.favicon
