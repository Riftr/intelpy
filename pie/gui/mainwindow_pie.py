#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
#from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget, QMessageBox
from pie.gui.MainWindow import Ui_MainWindow
from pathlib import Path
import getpass
import pie.gui.logformatting as log
import pie.eve.eveloghandler_worker as eveloghandler
from pie.eve.eveloghandler_signals import EveworkerSignals
import threading
import pie.gui.playalert_worker as playalertworker
import time

# Todo: fix multiple clients, improve file reading (from last line to known line), known line cleanup
# Todo: filter options (clear, status etc)

class MainWindow(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self, configuration, eve_data, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.configuration = configuration
        self.eve_data = eve_data
        self.signals = EveworkerSignals()
        self.event_stop = threading.Event()
        self.alert_system_names_readable = []
        self.update_alert_systems()  # update alert systems from config

        # Set initial state
        # Set home and log locations, force uppercase, numbers, hyphen in home field
        self.lineEditHome_System.setText(configuration.value["home_system"])
        self.lineEditEve_Log_Location.setText(configuration.value["eve_log_location"])
        self.lineEdit_alarm.setText(configuration.value["alarm_sound"])

        # Set checkboxes
        if self.configuration.value["display_alerts"]:
            self.checkbox_displayalerts.setChecked(True)
        if self.configuration.value["display_clear"]:
            self.checkBox_displayclear.setChecked(True)
        if self.configuration.value["display_all"]:
            self.checkBox_displayall.setChecked(True)

        # Set the channel list
        self.channelListWidget.addItems(configuration.value["watched_channels"])
        self.add_channel()

        # Set the alert slider
        self.horizontalSlider_AlertJumps.setValue(configuration.value["alert_jumps"])
        self.label_alertjumps.setText(str(configuration.value["alert_jumps"]))

        # Connections
        # Buttons
        self.pushButtonChoose_Eve_Log_Location.clicked.connect(self.choose_log_location)
        self.pushButtonSet_Home.clicked.connect(self.set_home)
        self.clearLogButton.clicked.connect(self.clear_log)
        self.addChannelAddButton.clicked.connect(self.add_channel)
        self.removeChannelButton.clicked.connect(lambda: self.remove_channel(self.channelListWidget.selectedItems()))

        # Advanced config
        self.pushButtonChoose_alarm_Location.clicked.connect(self.choose_alarm_location)
        self.checkbox_displayalerts.stateChanged.connect(
            lambda: self.checkbox_changed(self.checkbox_displayalerts, "display_alerts"))
        self.checkBox_displayclear.stateChanged.connect(
            lambda: self.checkbox_changed(self.checkBox_displayclear, "display_clear"))
        self.checkBox_displayall.stateChanged.connect(
            lambda: self.checkbox_changed(self.checkBox_displayall, "display_all"))

        # Alert silder
        self.horizontalSlider_AlertJumps.valueChanged.connect(self.alert_slider_changed)

        # Figure out where logs are stored
        if configuration.value["eve_log_location"] == "":
            if configuration.get_platform() == "unix":
                configuration.value["eve_log_location"] = str(Path.home()) + "/Games/eve-online/drive_c/users/" + \
                                                          getpass.getuser() + \
                                                          "/My Documents/EVE/logs/Chatlogs/"
            elif configuration.get_platform() == "windows":
                configuration.value["eve_log_location"] = str(Path.home()) + "c:/users/" + \
                                                          getpass.getuser() + \
                                                          "/My Documents/EVE/logs/Chatlogs/"
            else:
                self.error_message("IntelPy: Eve log file location",
                                     "Could not automatically figure out where your Eve logs are located.",
                                     "Please manually set this in the application for alerts to function.",
                                     "",
                                     "critical")
            self.lineEditEve_Log_Location.setText(configuration.value["eve_log_location"])
            self.configuration.flush_config_to_file()

        # Re-set home to calculate alerts
        self.set_home()

        # Watchdog worker thread to monitor logs
        #self.eveloghandler_worker = None
        self.eveloghandler_worker = eveloghandler.Eveloghandler_worker(self.configuration, self.event_stop)
        self.eveloghandler_worker.pass_message.connect(self.message_ready_process)
        self.start_watchdog()

    # Methods

    # Log options
    def checkbox_changed(self, state, which_button):
        alert_on = "set to <font color=\"green\">ON</font>"
        alert_off = "set to <font color=\"red\">OFF</font>"
        if which_button == "display_alerts":
            if state.isChecked():
                self.set_config_state("display_alerts", 1)
                self.append_log(log.format_info("Display alert details set to " + alert_on))
            else:
                self.set_config_state("display_alerts", 0)
                self.append_log(log.format_info("Display alert details set to " + alert_off))
        if which_button == "display_clear":
            if state.isChecked():
                self.set_config_state("display_clear", 1)
                self.append_log(log.format_info("Display clear set to " + alert_on))
            else:
                self.set_config_state("display_clear", 0)
                self.append_log(log.format_info("Display clear set to " + alert_off))
        if which_button == "display_all":
            if state.isChecked():
                self.set_config_state("display_all", 1)
                self.append_log(log.format_info("Display all set to " + alert_on))
            else:
                self.set_config_state("display_all", 0)
                self.append_log(log.format_info("Display all set to " + alert_off))

    # Alert slider
    def alert_slider_changed(self):
        slider_value = self.horizontalSlider_AlertJumps.value()
        self.append_log(log.format_important("Alert set to <font size=\"4\" color=\"#00ffff\">" + str(slider_value) +
                                             "</font> jumps from " + self.configuration.value["home_system"]))
        self.configuration.value["alert_jumps"] = slider_value
        self.label_alertjumps.setText(str(slider_value))
        # Regen alert systems
        self.generate_neigbourhood(int(slider_value), self.configuration.value["home_system"])
        self.configuration.flush_config_to_file()
        # Convert to readable names
        self.update_alert_systems()

    def update_alert_systems(self):
        self.alert_system_names_readable.clear()
        for system in self.configuration.value["alert_systems"]:
            self.alert_system_names_readable.append(self.eve_data.get_system_name(system))

    def generate_neigbourhood(self, jumps, home):
        id_code = self.eve_data.get_id_code(home)
        self.configuration.value["alert_systems"] = self.eve_data.get_neighbours_within(id_code, jumps)

    def set_config_state(self, key, value):
        # Used for setting non-list values in the config
        self.configuration.value[key] = value
        self.configuration.flush_config_to_file()

    def choose_log_location(self):
        self.log_location = QFileDialog.getExistingDirectory(
            self,
            "Choose Eve Log Files Directory",
            str(Path.home()),
            options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)

        if self.log_location != "":
            self.lineEditEve_Log_Location.setText(self.log_location)
            self.configuration.value["eve_log_location"] = self.log_location
            self.configuration.flush_config_to_file()
            self.append_log(log.format_info("Log directory set to: " + self.configuration.value["eve_log_location"]))
            self.restart_watchdog()

    def choose_alarm_location(self):
        self.alarm_location = QFileDialog.getOpenFileName(
            self,
            "Choose sound file",
            "pie/resources",
            "Sounds (*.mp3 *.wav)",
            options=QFileDialog.DontUseNativeDialog)

        if self.alarm_location[0]:
            self.lineEdit_alarm.setText(self.alarm_location[0])
            self.configuration.value["alarm_sound"] = self.alarm_location[0]
            self.configuration.flush_config_to_file()
            self.append_log(log.format_info("Alarm set to: " + self.configuration.value["alarm_sound"]))

    def set_home(self):
        # Check home value against list. If valid, set new home and calculate jumps from
        # If not valid, don't save/calculate and instead display a dialog
        # TODO: Provide suggestions as user types
        new_home = (self.lineEditHome_System.text()).upper()

        # Check if new home is valid
        if self.eve_data.is_valid_system(new_home):
            # New home valid
            self.configuration.value["home_system"] = new_home
            self.lineEditHome_System.setText(new_home)
            self.append_log(log.format_important("Home set to: " + self.configuration.value["home_system"]))
            self.generate_neigbourhood(self.horizontalSlider_AlertJumps.value(), self.configuration.value["home_system"])
            self.configuration.flush_config_to_file()
            self.update_alert_systems()
        else:
            # New home not valid
            old_home = self.configuration.value["home_system"]
            self.lineEditHome_System.setText(old_home.upper())
            self.error_message("PersonalIntel4Eve: Home not valid",
                               "The home system you entered, " + new_home + ", was not valid.",
                               "Please enter a valid system name.",
                               "",
                               "critical")

    def clear_log(self):
        self.logTextEdit.clear()

    def append_log(self, text):
        self.logTextEdit.append(text)

    def add_channel(self):
        is_dupe = False
        if self.lineEditChannelAdd.text() != "":
            for i in range(self.channelListWidget.count()):
                if self.channelListWidget.item(i).text() == self.lineEditChannelAdd.text():
                    is_dupe = True
            if not is_dupe:
                self.configuration.value["watched_channels"].append(self.lineEditChannelAdd.text())
                self.channelListWidget.addItem(self.lineEditChannelAdd.text())
                self.configuration.flush_config_to_file()
                self.append_log(log.format_info(self.lineEditChannelAdd.text() + " channel added"))
            self.lineEditChannelAdd.clear()
            # Reset watchdog patterns?
            self.eveloghandler_worker.set_patterns()

    def remove_channel(self, items):
        for item in items:
            removed_item = self.channelListWidget.takeItem(self.channelListWidget.row(item))
            self.configuration.value["watched_channels"].remove(removed_item.text())
            self.configuration.flush_config_to_file()
            self.append_log(log.format_info(removed_item.text() + " channel removed"))
            # Reset watchdog patterns?
            self.eveloghandler_worker.set_patterns()

    # Standard error messages
    def error_message(self, title, message, informative_text, details, icon="warning"):
        msg_dialog = QMessageBox()
        msg_dialog.setWindowTitle(title)
        msg_dialog.setText(message)
        msg_dialog.setInformativeText(informative_text)
        msg_dialog.setDetailedText(details)
        msg_dialog.setStandardButtons(QMessageBox.Ok)
        if icon == "critical":
            msg_dialog.setIcon(QMessageBox.Critical)
        else:
            msg_dialog.setIcon(QMessageBox.Warning)
        msg_dialog.exec_()

    # Logs watchdog functions
    def start_watchdog(self):
        self.eveloghandler_worker.start()
        #self.eveloghandler_worker.pass_message.connect(self.message_ready_process)

    #@pyqtSlot()
    def stop_watchdog(self):
        self.event_stop.set()

    def restart_watchdog(self):
        self.stop_watchdog()
        time.sleep(1.1)
        self.event_stop.clear()
        self.start_watchdog()

    @pyqtSlot(list)
    def message_ready_process(self, message_list):
        #here we can check alerts, update UI etc
        # message_list =  dts, nick, message
        this_message = message_list[2]
        this_message = this_message.upper()

        if message_list[3] >= 1:
            self.append_log(log.format_important("Note, " + str(message_list[3] - 1) +
                                                 " lines were updated since last run"))

        # check for clear
        if "CLEAR" in this_message or "CLR" in this_message:
            if self.configuration.value["display_clear"]:
                self.append_log(log.format_info("Clear message received: " + message_list[2]))
            return

        # check if message contains a system within jump range
        for system in self.alert_system_names_readable:
            if system in this_message:
                # display alert msg
                self.append_log(log.format_alert("Bad guy reported within " +
                                                 str(self.configuration.value["alert_jumps"]) +
                                                 " jumps!"
                                                 ))
                #check if details need to be printed
                if self.configuration.value["display_alerts"]:   # for some reason this waits til sound plays sometimes
                    self.append_log(log.format_important("matched: " + system))
                    self.append_log("<b> > </b> " + log.format_info(str(message_list[0])))
                    self.append_log(log.format_info(message_list[2]))

                # play alert (blocking on Linux so threading it)
                self.playalert_worker = playalertworker.PlayAlert_worker(self.configuration)
                self.playalert_worker.start()
                return

        # Display all?
        if self.configuration.value["display_all"]:
            self.append_log("<b> > </b> " + log.format_info(str(message_list[0])))
            self.append_log(log.format_info(message_list[2]))







