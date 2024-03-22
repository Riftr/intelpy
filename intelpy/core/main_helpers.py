import os
from sys import platform

def default_json_config(resources_dir):
    default_json = {
        "home_system": "1DQ1-A",
        "eve_log_location": "",
        "watched_channels": [
            "delve.imperium",
            "querious.imperium",
            "ftn.imperium",
            "vnl.imperium",
            "cr.imperium",
            "aridia.imperium",
            "khanid.imperium",
            "lone.imperium"
        ],
        "alert_jumps": 3,
        "alert_systems": [],
        "log_watch_active": 1,
        "config_loc": "",
        "alarm_sound": str(resources_dir) + os.sep + "alarm2.mp3",
        "display_alerts": 1,
        "display_clear": 1,
        "display_all": 1,
        "filter_status": 1,
        "filter_clear": 1,
        "debug": 0,
        "message_timeout": 1.0,
        "alert_timeout": 5,
        "dark_theme": 0
    }
    return default_json

def discover_resources_dir(script_dir):
    if os.path.exists(os.path.join(script_dir, "resources")):    # windows/default use resources folder local to executable
        resources_dir = os.path.join(script_dir, "resources")
    elif os.path.exists(os.path.join(script_dir, "intelpy", "resources")):  # old directory on previous versions
        resources_dir = os.path.join(script_dir, "intelpy", "resources")
    elif platform.startswith("linux") or platform.startswith("freebsd") or platform.startswith("darwin"):
        resources_dir = os.path.join("usr", "share", "intelpy")  # on posix use /usr/share/intelpy
    else:
        print("IntelPy could not find resources directory.")
        raise OSError(2, "IntelPy could not find the resources directory", "resources")
    return resources_dir




