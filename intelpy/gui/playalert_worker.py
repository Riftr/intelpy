from PyQt5.QtCore import QThread
from playsound import playsound

class PlayAlert_worker(QThread):
    def __init__(self, configuration, *args, **kwargs):
        super(PlayAlert_worker, self).__init__(*args, **kwargs)
        # Watchdog
        self.configuration = configuration

    def run(self):
        playsound(self.configuration.value["alarm_sound"])