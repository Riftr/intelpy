from PyQt5.QtCore import *
import intelpy.eve.eveloghandler as eveloghandler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import time

class Eveloghandler_worker(QThread):
    pass_message = pyqtSignal(list)

    def __init__(self, configuration, event_stop, *args, **kwargs):
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

    @pyqtSlot()
    def run(self):
        # Eveloghandler
        self.eveloghandler_watchdog = eveloghandler.EveLogHandler(self.watched_channels, self.ignore_patterns,
                                                                  self.ignore_directories, self.case_sensitive,
                                                                  self.configuration)
        self.eveloghandler_watchdog.message_ready.connect(self.test_catch_connection)
        # Observer
        self.watchdog_observer = Observer()
        self.watchdog_observer.schedule(self.eveloghandler_watchdog,
                                        self.configuration.value['eve_log_location'], False)
        self.watchdog_observer.start()

        while not self.event_stop.is_set():
            time.sleep(1)

        # when stopping
        self.eveloghandler_watchdog.pickle_dict()
        self.watchdog_observer.stop()

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
            return_list.append(first_slash + channel + ".imperium*")

        return return_list

    @pyqtSlot(list)
    def test_catch_connection(self, this_list):
        # This slot just bubbles our message up to the main UI thread
        self.pass_message.emit(this_list)
