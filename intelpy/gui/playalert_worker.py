from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
import playsound


class PlayAlert_worker(QThread):
    def __init__(self, configuration, logger=None, *args, **kwargs):
        super(PlayAlert_worker, self).__init__(*args, **kwargs)
        # Watchdog
        self.configuration = configuration
        self.logger = logger

    def run(self):
        alarm_sound = self.configuration.value["alarm_sound"]
        try:
            playsound.playsound(str(alarm_sound))
            # note: for some reason when playsound errors it does not respect try/catch blocks and just prints
            # an error with an error code then silently crashes
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
