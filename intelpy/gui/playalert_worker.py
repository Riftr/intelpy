from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
from playsound import playsound, PlaysoundException


class PlayAlert_worker(QThread):
    def __init__(self, configuration, logger=None, *args, **kwargs):
        super(PlayAlert_worker, self).__init__(*args, **kwargs)
        # Watchdog
        self.configuration = configuration
        self.logger = logger

    def run(self):
        alarm_sound = self.configuration.value["alarm_sound"]
        try:
            self.logger.write_log("Trying to play alarm sound...")
            playsound(str(alarm_sound))
            # note: when playsound errors on windows it does not seem respect try/catch blocks and just prints
            # an error with an error code then silently crashes
        except PlaysoundException as e:
            if self.logger:
                self.logger.write_log("Error: Playsound module error code: ", str(e))
            self.error_diag("Error: Playsound module error code: ", str(e))
        except FileNotFoundError as e:
            if self.logger:
                self.logger.write_log("Error: Could not play alert sound! File not found.", str(e))
            self.error_diag("Error: Could not play alert sound! File not found.", str(e))
        except Exception as e:
            if self.logger:
                self.logger.write_log("Error: Could not play alert sound!", str(e))
            self.error_diag("Error: Could not play alert sound!", str(e))

    def error_diag(self, message, error):
        msg_dialog = QMessageBox()
        msg_dialog.setWindowTitle("Alert sound error")
        msg_dialog.setText(message)
        msg_dialog.setDetailedText(error)
        msg_dialog.setInformativeText(self.configuration.value["alarm_sound"])
        msg_dialog.setStandardButtons(QMessageBox.Ok)
        msg_dialog.setIcon(QMessageBox.Warning)
        msg_dialog.exec_()
