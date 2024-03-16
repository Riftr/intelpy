from PyQt5.QtCore import QThread
#from PyQt5 import QtWidgets
from pygame import mixer


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
               mixer.init()
               mixer.music.load(alarm_sound)
               mixer.music.play()
        except Exception as e:
            if self.logger is not None:
                self.logger.write_log("Error: Could not play alert sound! " + str(e))
            #self.error_diag("Error: Could not play alert sound!", str(e))
            raise

    #def error_diag(self, message, error):
    #    print("Intelpy " + message + str(error))
    #    #pop up gui error msg
    #    app = QtWidgets.QApplication([])
    #    error_diag = QtWidgets.QErrorMessage()
    #    error_diag.setWindowTitle("IntelPy: Alert sound error")
    #    error_diag.showMessage('IntelPy ended with an error: \n ' + str(error))
    #    app.exec_()
    #    raise
