#!/usr/bin/env python3
import sys
from intelpy import config
from intelpy.gui import mainwindow_intelpy
import intelpy.eve.evedata as evedata
from PyQt5.QtWidgets import QApplication
from tests import debug_config


def main():
    app_name = "IntelPy"

    # Set the default configuration
    default_json = {
        "home_system": "NIDJ-K",
        "eve_log_location": "",
        "watched_channels": [
            "delve",
            "querious",
            "ftn",
            "vnl",
            "cr",
            "aridia",
            "khanid",
            "lone"
        ],
        "alert_jumps": 3,
        "alert_systems": [],
        "log_watch_active": 1,
        "config_loc": "",
        "alarm_sound": "intelpy/resources/alarm2.mp3",
        "display_alerts": 1,
        "display_clear": 1,
        "display_all": 1,
        "filter_status": 1,
        "filter_clear": 1,
        "debug": 1,
        "message_timeout": 1.0,
        "alert_timeout": 5
    }

    configuration = config.Config(app_name, default_json)
    configuration.value["config_loc"] = configuration.file_location

    if configuration.value["debug"]:
        print("---- IntelPy ----")
        print("Debug enabled..")

    # Load eve data
    eve_data_file = "intelpy/resources/evedata.p"
    eve_systems = "intelpy/resources/systems.p"
    eve_idstosystems = "intelpy/resources/idtosystems.p"
    eve_data = evedata.EveData(eve_data_file, eve_systems, eve_idstosystems)

    if configuration.value["debug"]:
        print("---- Configuration on loading ----")
        print("eve_data_file: " + eve_data_file)
        print("eve_systems: " + eve_systems)
        print("eve_idstosystems: " + eve_idstosystems)
        debug_config.debug_config(configuration)

    # Load main window GUI
    app = QApplication(sys.argv)
    window = mainwindow_intelpy.MainWindow(configuration, eve_data)
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


