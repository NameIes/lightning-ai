import winreg
import vdf
from pathlib import Path


CS2_APP_ID = '730'
STEAM_REGISTRY_KEY = "SOFTWARE\\WOW6432Node\\Valve\\Steam"
CS2_PATH = "steamapps\\common\\Counter-Strike Global Offensive"
GSI_PATH = "game\\csgo\\cfg\\gamestate_integration_GSI.cfg"
LIBRARY_FOLDERS_PATH = "steamapps\\libraryfolders.vdf"
APP_MANIFEST_PATH = f"steamapps\\appmanifest_{CS2_APP_ID}.acf"


def get_steam_path() -> Path:
    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, STEAM_REGISTRY_KEY)
    steam_path = winreg.QueryValueEx(hkey, "InstallPath")[0]
    winreg.CloseKey(hkey)
    return Path(steam_path)


def get_steam_library_path(steam_path: Path) -> Path:
    library_folders = vdf.load(open(steam_path / LIBRARY_FOLDERS_PATH))[
        "libraryfolders"
    ]
    for key in library_folders:
        if str(CS2_APP_ID) in library_folders[key]["apps"]:
            return Path(library_folders[key]["path"])

    raise FileNotFoundError()


def get_cs2_path() -> Path:
    return get_steam_library_path(get_steam_path()) / CS2_PATH


def get_gsi_config_path() -> Path:
    return get_cs2_path() / GSI_PATH
