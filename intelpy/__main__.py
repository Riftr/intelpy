#!/usr/bin/env python3
import sys
from intelpy import config
from intelpy.gui import mainwindow_intelpy
import intelpy.eve.evedata as evedata
from PyQt5.QtWidgets import QApplication


def main():
    debug = False
    app_name = "intelpy"

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
        "alarm_sound": "intelpy/resources/sounds/alarm4.mp3",
        "display_alerts": 0,
        "display_clear": 1,
        "display_all": 0
    }

    configuration = config.Config(app_name, default_json)
    configuration.value["config_loc"] = configuration.file_location

    # Load eve data
    eve_data = "intelpy/resources/evedata.p"
    eve_systems = "intelpy/resources/systems.p"
    eve_idstosystems = "intelpy/resources/idtosystems.p"
    eve_data = evedata.EveData(eve_data, eve_systems, eve_idstosystems)

    print("starting")
    # Load main window GUI
    app = QApplication(sys.argv)
    window = mainwindow_intelpy.MainWindow(configuration, eve_data)
    window.show()
    app.exec_()

    # Shouldn't be executed until GUI closed
    #if debug:
    #    debug_config.debug_config(configuration)

    # Flush configuration
    configuration.flush_config_to_file()
    window.stop_watchdog()
    print("ending")


if __name__ == '__main__':
    main()


