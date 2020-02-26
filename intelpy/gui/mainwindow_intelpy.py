from PyQt5.QtCore import pyqtSlot, QTimer, QThreadPool
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget, QMessageBox
from intelpy.gui.MainWindow import Ui_MainWindow
from pathlib import Path
import getpass
import intelpy.gui.logformatting as log
import intelpy.eve.eveloghandler_worker as eveloghandler
from intelpy.eve.eveloghandler_signals import EveworkerSignals
import threading
import intelpy.gui.playalert_worker as playalertworker
import time
from datetime import datetime
from collections import deque


class MainWindow(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self, configuration, eve_data, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.configuration = configuration
        self.eve_data = eve_data
        self.signals = EveworkerSignals()
        self.event_stop = threading.Event()
        self.alert_system_names_readable = []
        self.update_alert_systems()  # update alert systems from config
        self.threadpool = QThreadPool()

        # Eve Time
        self.eve_time_statusbar()
        self.evetimer = QTimer(self)
        self.evetimer.timeout.connect(self.eve_time_statusbar)
        self.evetimer.start(10000)  # ms

        # Recent alerts timer
        self.recent_alerts_timer = QTimer(self)
        self.recent_alerts_timer.timeout.connect(self.alert_recent_update)
        self.recent_alerts_timer.start(10000)  # ms
        self.recent_alerts = deque()

        # Set initial state
        # Set home and log locations, force uppercase, numbers, hyphen in home field
        self.lineEditHome_System.setText(self.configuration.value["home_system"])
        self.lineEditEve_Log_Location.setText(self.configuration.value["eve_log_location"])
        self.lineEdit_alarm.setText(self.configuration.value["alarm_sound"])
        self.spinBox_recentalerttimeout.setValue(self.configuration.value["alert_timeout"])  # mins

        # Set checkboxes
        if self.configuration.value["display_alerts"]:
            self.checkbox_displayalerts.setChecked(True)
        if self.configuration.value["display_clear"]:
            self.checkBox_displayclear.setChecked(True)
        if self.configuration.value["display_all"]:
            self.checkBox_displayall.setChecked(True)
        if self.configuration.value["filter_clear"]:
            self.checkBox_filterclear.setChecked(True)
        if self.configuration.value["filter_status"]:
            self.checkBox_filterstatus.setChecked(True)

        # Set the channel list
        self.channelListWidget.addItems(self.configuration.value["watched_channels"])
        self.add_channel()

        # Set the alert slider
        self.horizontalSlider_AlertJumps.setValue(self.configuration.value["alert_jumps"])
        self.label_alertjumps.setText(str(self.configuration.value["alert_jumps"]))

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
        self.checkBox_filterclear.stateChanged.connect(
            lambda: self.checkbox_changed(self.checkBox_filterclear, "filter_clear"))
        self.checkBox_filterstatus.stateChanged.connect(
            lambda: self.checkbox_changed(self.checkBox_filterstatus, "filter_status"))

        # Alert silder
        self.horizontalSlider_AlertJumps.valueChanged.connect(self.alert_slider_changed)

        # Timeout spinner
        self.spinBox_recentalerttimeout.valueChanged.connect(self.recent_alert_spinbox_changed)

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
        self.eveloghandler_worker = eveloghandler.Eveloghandler_worker(self.configuration, self.event_stop)
        self.eveloghandler_worker.pass_message.connect(self.message_ready_process)
        self.start_watchdog()

        # Set recent alerts to blank
        self.label_recentalert1.setText("")
        self.label_recentalert2.setText("")
        self.label_recentalert3.setText("")
        self.label_recentalert4.setText("")
        self.label_recentalert5.setText("")

    # Methods
    def recent_alert_spinbox_changed(self):
        spinbox_value = self.spinBox_recentalerttimeout.value()
        self.configuration.value["alert_timeout"] = spinbox_value
        self.configuration.flush_config_to_file()

    def alert_recent_update(self):
        # Updates the recent alert UI
        for alert in self.recent_alerts:
            alert[0] += 5

        if self.configuration.value["debug"]:
            print(self.recent_alerts)
        # timer - system - jumps
        # clear alerts
        self.label_recentalert1.setText("")
        self.label_recentalert2.setText("")
        self.label_recentalert3.setText("")
        self.label_recentalert4.setText("")
        self.label_recentalert5.setText("")
        if len(self.recent_alerts) == 0:
            return   # no alerts
        # pop off old alert
        if self.recent_alerts[0][0] > self.configuration.value["alert_timeout"] * 60:
            self.recent_alerts.popleft()
        if len(self.recent_alerts) >= 1:
            self.label_recentalert1.setText(self.alert_create_text(self.recent_alerts[0]) +
                                            "\n<br>" + self.recent_alerts[0][3])
        if len(self.recent_alerts) >= 2:
            self.label_recentalert2.setText(self.alert_create_text(self.recent_alerts[1]) +
                                            "\n<br>" + self.recent_alerts[1][3])
        if len(self.recent_alerts) >= 3:
            self.label_recentalert3.setText(self.alert_create_text(self.recent_alerts[2]) +
                                            "\n<br>" + self.recent_alerts[2][3])
        if len(self.recent_alerts) >= 4:
            self.label_recentalert4.setText(self.alert_create_text(self.recent_alerts[3]) +
                                            "\n<br>" + self.recent_alerts[3][3])
        if len(self.recent_alerts) >= 5:
            self.label_recentalert5.setText(self.alert_create_text(self.recent_alerts[4]) +
                                            "\n<br>" + self.recent_alerts[4][3])

    def alert_create_text(self, alert_list):
        if alert_list[0] < 60:
            alert_timer = "<br><font color=\"red\" size=\"4\"><b>&lt;1 min &nbsp;&nbsp; </b></font>"
        else:
            secs_to_mins = alert_list[0] / 60
            alert_timer = "<br><b>" + str(secs_to_mins).split(".")[0] + " mins &nbsp;</b>"

        alert_txt = alert_list[1] + " &nbsp;&nbsp; <b>" + alert_list[2] + "</b> jumps"
        return alert_timer + alert_txt

    def alert_recent_add(self, secs, system, jumps, message):
        # Add a new alert to the UI
        if len(self.recent_alerts) == 5:  # 2d list
            self.recent_alerts.popleft()  # remove the oldest one
        self.recent_alerts.append([secs, system, jumps, message])  # add a list to the list
        self.alert_recent_update()

    def eve_time_statusbar(self):
        # Updates the time in the status, percice to 10 seconds (don't need anything faster tbh)
        self.eve_statusbar.showMessage("Eve time: " + str(self.get_eve_time()), 10000)

    def get_eve_time(self):
        return datetime.utcnow().strftime("%H:%M %d/%m/%Y")

    # Log options
    def checkbox_changed(self, state, which_button):
        alert_on = "set to <font color=\"green\">ON</font>"
        alert_off = "set to <font color=\"red\">OFF</font>"
        ignore_on = "set to <font color=\"red\">IGNORE</font>"
        ignore_off = "set to <font color=\"green\">NOT IGNORE</font>"
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
        if which_button == "filter_clear":
            if state.isChecked():
                self.set_config_state("filter_clear", 1)
                self.append_log(log.format_info("Clear messages set to " + ignore_on))
            else:
                self.set_config_state("filter_clear", 0)
                self.append_log(log.format_info("Clear messages set to " + ignore_off))
        if which_button == "filter_status":
            if state.isChecked():
                self.set_config_state("filter_status", 1)
                self.append_log(log.format_info("Status messages set to " + ignore_on))
            else:
                self.set_config_state("filter_status", 0)
                self.append_log(log.format_info("Status messages set to " + ignore_off))

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
            "intelpy/resources",
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

        # check for clear
        if self.configuration.value["filter_clear"]:
            if "CLEAR" in this_message or "CLR" in this_message:
                if self.configuration.value["display_clear"]:
                    self.append_log(log.format_info("Clear message received: " + message_list[2]))
                return

        if self.configuration.value["filter_status"]:
            if "STATUS" in this_message:
                self.append_log(log.format_info("Status? message received: " + message_list[2]))
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
                if self.configuration.value["display_alerts"]:
                    self.append_log(log.format_important("<font color=\"red\">Time: </font>" + str(message_list[0])))
                    self.append_log(log.format_important("<font color=\"red\">System: </font>" + system))
                    self.append_log(log.format_important("<font color=\"red\">Reported by: </font>" + message_list[1]))
                    self.append_log(log.format_important("<font color=\"red\">Message: </font>" + message_list[2]))

                # play alert (blocking on Linux so threading it)
                self.playalert_worker = playalertworker.PlayAlert_worker(self.configuration)
                self.playalert_worker.start()
                # get id codes
                system_id = self.eve_data.get_id_code(system)
                home_id = self.eve_data.get_id_code(self.lineEditHome_System.text())
                short_path = self.eve_data.shortest_path_length(home_id, system_id)
                # secs, reported system, jumps, msg
                self.alert_recent_add(0, system, str(short_path), message_list[2])
                return

        # Display all?
        if self.configuration.value["display_all"]:
            self.append_log("<b> > </b> " + log.format_info(str(message_list[0])))
            self.append_log(log.format_info(message_list[2]))







