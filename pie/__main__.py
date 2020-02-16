#!/usr/bin/env python3
import sys
from pie import config
from pie.gui import mainwindow_pie
import pie.eve.evedata as evedata
from PyQt5.QtWidgets import QApplication
from tests import debug_config

# Todo: better log file handling - use known files and line up to instead of just getting last line

def main():
    app_name = "PersonalIntel4Eve"

    # Set the default configuration
    default_json = {
        "home_system": "NIDJ-K",
        "eve_log_location": "",
        "watched_channels": [
            "delve",
            "querious"
        ],
        "alert_jumps": 2,
        "alert_systems": [],
        "log_watch_active": 1,
        "config_loc": "",
        "alarm_sound": "pie/resources/alarm2.mp3",
        "display_alerts": 0,
        "display_clear": 1,
        "display_all": 0,
        "debug": 1,
        "message_timeout": 10
    }

    configuration = config.Config(app_name, default_json)
    configuration.value["config_loc"] = configuration.file_location

    if configuration.value["debug"]:
        print("---- PersonalIntel4Eve ----")
        print("Debug enabled..")

    # Load eve data
    eve_data_file = "pie/resources/evedata.p"
    eve_systems = "pie/resources/systems.p"
    eve_idstosystems = "pie/resources/idtosystems.p"
    eve_data = evedata.EveData(eve_data_file, eve_systems, eve_idstosystems)

    if configuration.value["debug"]:
        print("---- Configuration on loading ----")
        print("eve_data_file: " + eve_data_file)
        print("eve_systems: " + eve_systems)
        print("eve_idstosystems: " + eve_idstosystems)
        debug_config.debug_config(configuration)

    # Load main window GUI
    app = QApplication(sys.argv)
    window = mainwindow_pie.MainWindow(configuration, eve_data)
    window.show()
    app.exec_()

    if configuration.value["debug"]:
        print("---- Configuration after closing ----")
        debug_config.debug_config(configuration)

    # Flush configuration
    configuration.flush_config_to_file()
    window.stop_watchdog()


if __name__ == '__main__':
    main()


