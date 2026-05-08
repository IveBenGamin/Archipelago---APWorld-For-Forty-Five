# TODO maybe use this once I understand auto-connect better
import os
import webbrowser

from worlds.LauncherComponents import Component, Type, components

STEAM_APP_ID = "2691350"
_CONNECT_FILE = os.path.expanduser("~/forty-five-ap-connect.txt")


def run_client(*args: str) -> None:
    uri = next((a for a in args if a.startswith("archipelago://")), None)
    if uri:
        _write_connect_file(uri)
    webbrowser.open(f"steam://rungameid/{STEAM_APP_ID}")


def _write_connect_file(uri: str) -> None:
    # URI format: archipelago://SlotName:password@host:port
    try:
        without_scheme = uri[len("archipelago://"):]
        userinfo, hostport = without_scheme.rsplit("@", 1) if "@" in without_scheme else ("", without_scheme)
        slot, password = userinfo.split(":", 1) if ":" in userinfo else (userinfo, "")
        with open(_CONNECT_FILE, "w") as f:
            f.write(f"host={hostport}\n")
            f.write(f"slot={slot}\n")
            f.write(f"password={password}\n")
    except Exception:
        pass


components.append(
    Component(
        "Forty-Five",
        func=run_client,
        game_name="Forty-Five",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)