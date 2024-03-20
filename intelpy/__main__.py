#!/usr/bin/env python3
import sys
from intelpy import config
from intelpy.gui import mainwindow_intelpy
import intelpy.eve.evedata as evedata
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
import os
import intelpy.logging.logger
from intelpy.logging import logrotate

def main():
    app_name = "IntelPy"
    #os.path.dirname(__file__)
    script_dir = os.getcwd()
    if os.path.exists(os.path.join(script_dir, "resources")):
        resources_dir = os.path.join(script_dir, "resources")  # new directory
    else:
        resources_dir = os.path.join(script_dir, "intelpy", "resources")  # old directory or run from source
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
        "dark_theme": 0
    }

    configuration = config.Config(app_name, default_json)
    configuration.value["config_loc"] = configuration.file_location

    ''' Debug mode - set to 0 for release
        logged to debug.log if enabled and also enables console logs
        error message will often be separate'''
    # when this is set to 0 the app often crashes at weird places. Probably because logger object doesn't exist
    # something is probably using it without checking if it's None
    # weird thing is though it works fine when Pycharm is in debug mode itself regardless of this setting!
    configuration.value["debug"] = 1  #quick fix - just leave it at 1 and disable console mode on Windows pyinstaller

    # Rotate debug log
    if configuration.value["debug"]:
        debug_file = configuration.value["config_loc"] + "debug.log"
        moved_debug_file = configuration.value["config_loc"] + "debug.log.1"
        if logrotate.check_log_size(debug_file):
            logrotate.rotate_log_file(debug_file, moved_debug_file)

    # start logging to debug
    if configuration.value["debug"]:
        logger = intelpy.logging.logger.logger(app_name)
        logger.write_log("== New instance of IntelPy Started ==")
        print("---- IntelPy ----")
        print("Debug enabled. See debug.log for output.")
        logger.write_log("Loading Eve data..")
    else:
        logger = None


    # Load eve data
    eve_data_file = str(resources_dir) + os.sep + "evedata.p"
    eve_systems = str(resources_dir) + os.sep + "systems.p"
    eve_idstosystems = str(resources_dir) + os.sep + "idtosystems.p"
    eve_data = evedata.EveData(eve_data_file, eve_systems, eve_idstosystems)

    if configuration.value["debug"] and logger is not None:
        logger.write_log("---- Configuration on loading ----")
        logger.write_log("eve_data_file: " + eve_data_file)
        logger.write_log("eve_systems: " + eve_systems)
        logger.write_log("eve_ids to systems: " + eve_idstosystems)
        #debug_config.debug_config(configuration)
        logger.debug_config(configuration)

    # Load main window GUI
    intelpyapp = QApplication(sys.argv)

    # Nice dark theme if the user wishes to use it
    if 'dark_theme' not in configuration.value:
        configuration.value['dark_theme'] = 0
        configuration.flush_config_to_file()

    if configuration.value['dark_theme'] == 1:
        if configuration.value["debug"] and logger is not None:
            logger.write_log("Dark theme was enabled")
        intelpyapp.setStyle("Fusion")
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
        intelpyapp.setPalette(palette)

    window = mainwindow_intelpy.MainWindow(configuration, eve_data, logger)
    window.show()
    intelpyapp.exec_()  # crash sometimes on windows here

    if configuration.value["debug"] and logger is not None:
        logger.write_log("---- Configuration after closing ----")
        logger.debug_config(configuration)
        logger.write_log("== This instance of IntelPy closed ==")

    # Flush configuration (prob don't need this)
    #configuration.value["debug"] = 0

    configuration.flush_config_to_file()
    window.stop_watchdog()

if __name__ == '__main__':
    main()


