from PyQt5.QtCore import QThread
from PyQt5 import QtWidgets
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
            if self.logger is not None:
               self.logger.write_log("Trying to play alarm sound...")
            playsound(str(alarm_sound))
            # note: when playsound errors on windows it does not seem respect try/catch blocks and just prints
            # an error with an error code then silently crashes
        #except PlaysoundException as e:
        #    if self.logger is not None:
        #        self.logger.write_log("Error: Playsound module error code: ", str(e))
        #    self.error_diag("Error: Playsound module error code: ", str(e))
        except FileNotFoundError as e:
            if self.logger is not None:
                self.logger.write_log("Error: Could not play alert sound! File not found.", str(e))
            self.error_diag("Error: Could not play alert sound! File not found.", str(e))
            raise
        except Exception as e:
            if self.logger is not None:
                self.logger.write_log("Error: Could not play alert sound!", str(e))
            self.error_diag("Error: Could not play alert sound!", str(e))
            raise

    def error_diag(self, message, error):
        print("Intelpy " + message + str(error))
        #pop up gui error msg
        app = QtWidgets.QApplication([])
        error_diag = QtWidgets.QErrorMessage()
        error_diag.setWindowTitle("IntelPy: Alert sound error")
        error_diag.showMessage('IntelPy ended with an error: \n ' + str(error))
        app.exec_()
        raise
