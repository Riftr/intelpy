#!/usr/bin/env python3
import sys
from intelpy import config
from intelpy.gui import mainwindow_intelpy
from intelpy.core import main_helpers
import intelpy.eve.evedata as evedata
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
import os
import intelpy.logging.logger
from intelpy.logging import logrotate



def main():
    app_name = "IntelPy"

    # get application root directory from this file's location
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)  # cx_Freeze frozen
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))  # Other packers

    # set resources dir based on app root/platform
    resources_dir = main_helpers.discover_resources_dir(script_dir)

    # Set the default configuration
    configuration = config.Config(app_name, main_helpers.default_json_config(resources_dir))
    configuration.value["config_loc"] = configuration.file_location
    configuration.value["debug"] = 1

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
    else:
        logger = None

    # Load eve data
    eve_data_file = str(resources_dir) + os.sep + "evedata.p"
    eve_systems = str(resources_dir) + os.sep + "systems.p"
    eve_idstosystems = str(resources_dir) + os.sep + "idtosystems.p"
    eve_data = evedata.EveData(eve_data_file, eve_systems, eve_idstosystems)

    if configuration.value["debug"] and logger is not None:
        logger.write_log("---- Configuration on loading ----")
        logger.write_log("Exe directory: " + str(script_dir))
        logger.write_log("Resources directory: " + str(resources_dir))
        logger.write_log("eve_data_file: " + eve_data_file)
        logger.write_log("eve_systems: " + eve_systems)
        logger.write_log("eve_ids to systems: " + eve_idstosystems)
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

    configuration.flush_config_to_file()
    window.stop_watchdog()

if __name__ == '__main__':
    main()


