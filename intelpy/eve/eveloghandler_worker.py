from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import intelpy.eve.eveloghandler as eveloghandler
from watchdog.observers import Observer
import time
import glob
from pathlib import Path as oldpath


def worker_error(error_msg):
    app = QtWidgets.QApplication([])
    error_diag = QtWidgets.QErrorMessage()
    error_diag.setWindowTitle("IntelPy Error")
    error_diag.showMessage('IntelPy ended with an error: \n ' + str(error_msg))
    app.exec_()

class Eveloghandler_worker(QThread):
    pass_message = pyqtSignal(list)

    def __init__(self, configuration, event_stop, logger=None, *args, **kwargs):
        super(Eveloghandler_worker, self).__init__(*args, **kwargs)
        # Watchdog
        self.configuration = configuration
        self.watched_channels = self.watched_channels_to_wildcards()
        self.ignore_directories = True
        self.case_sensitive = False
        self.ignore_patterns = None
        self.eveloghandler_watchdog = None
        self.watchdog_observer = None
        self.watched_channels = self.watched_channels_to_wildcards()
        self._running = False
        self.event_stop = event_stop
        self.platform = self.configuration.get_platform()
        self.toucher = None
        self.logger = logger

    @pyqtSlot()
    def run(self):
        try:
            # this is None if it's not set by the user or auto-detection fails or Eve isn't installed
            while self.configuration.value["eve_log_location"] is None:
                time.sleep(2)

            # Eveloghandler
            self.eveloghandler_watchdog = eveloghandler.EveLogHandler(self.watched_channels, self.ignore_patterns,
                                                                      self.ignore_directories, self.case_sensitive,
                                                                      self.configuration, self.logger)
            self.eveloghandler_watchdog.message_ready.connect(self.test_catch_connection)
            # Observer
            self.watchdog_observer = Observer()
            self.watchdog_observer.schedule(self.eveloghandler_watchdog,
                                            self.configuration.value['eve_log_location'], False)
            self.watchdog_observer.start()

            while not self.event_stop.is_set():
                # Windows workaround - for some reason Eve doesn't trigger the watchdog modify event on Windows.
                if self.platform == "windows":
                    log_path = self.configuration.value["eve_log_location"]
                    log_files = glob.glob(log_path + "/*")
                    for file in log_files:
                        oldpath(file).touch()
                    time.sleep(2)
                else:
                    time.sleep(1)

            # when stopping
            self.eveloghandler_watchdog.pickle_dict()
            self.watchdog_observer.stop()
        except Exception as e:
            print("IntelPy worker encountered an error: \n" + str(e))
            worker_error(str(e))
            raise SystemExit

    def set_patterns(self):
        # try to update the pattern list
        self.eveloghandler_watchdog.update_patterns(self.watched_channels_to_wildcards())

    def print_current_patterns(self):
        self.eveloghandler_watchdog.print_current_patterns()

    def watched_channels_to_wildcards(self):
        return_list = []
        first_slash = "*/"
        if self.configuration.get_platform == "windows":
            first_slash = "*\\"
        for channel in self.configuration.value["watched_channels"]:
            return_list.append(first_slash + channel + "*")

        return return_list

    @pyqtSlot(list)
    def test_catch_connection(self, this_list):
        # This slot just bubbles our message up to the main UI thread
        if self.configuration.value["debug"] and self.logger is not None:
            self.logger.write_log("Bubbling message from worker")
        self.pass_message.emit(this_list)
