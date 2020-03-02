#!/usr/bin/env python3
import sys
from intelpy import config
from intelpy.gui import mainwindow_intelpy
import intelpy.eve.evedata as evedata
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from tests import debug_config
import os

def main():
    app_name = "IntelPy"
    #os.path.dirname(__file__)
    script_dir = os.getcwd()
    resources_dir = os.path.join(script_dir, "intelpy", "resources")
    # Set the default configuration
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
        "windows_dark_theme": 0
    }

    configuration = config.Config(app_name, default_json)
    configuration.value["config_loc"] = configuration.file_location

    if configuration.value["debug"]:
        print("---- IntelPy ----")
        print("Debug enabled..")

    # Load eve data
    eve_data_file = str(resources_dir) + os.sep + "evedata.p"
    eve_systems = str(resources_dir) + os.sep + "systems.p"
    eve_idstosystems = str(resources_dir) + os.sep + "idtosystems.p"
    eve_data = evedata.EveData(eve_data_file, eve_systems, eve_idstosystems)

    if configuration.value["debug"]:
        print("---- Configuration on loading ----")
        print("eve_data_file: " + eve_data_file)
        print("eve_systems: " + eve_systems)
        print("eve_idstosystems: " + eve_idstosystems)
        debug_config.debug_config(configuration)

    # Load main window GUI
    app = QApplication(sys.argv)

    # Nice dark theme for windows, assume linux users know how to set it themselves
    if configuration.get_platform() == "windows" and configuration.value['windows_dark_theme'] == 1:
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

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


