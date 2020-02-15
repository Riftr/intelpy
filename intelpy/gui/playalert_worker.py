from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play


class PlayAlert_worker(QThread):
    def __init__(self, configuration, *args, **kwargs):
        super(PlayAlert_worker, self).__init__(*args, **kwargs)
        # Watchdog
        self.configuration = configuration

    def run(self):
        audio_file = None
        alarm_sound = self.configuration.value["alarm_sound"]
        try:
            if Path(alarm_sound).suffix == ".wav":
                audio_file = AudioSegment.from_wav(alarm_sound)
            elif Path(alarm_sound).suffix == ".mp3":
                audio_file = AudioSegment.from_mp3(alarm_sound)
            else:
                self.error_diag("Could not play alert sound as file format was not understood.",
                                "Check the file format is a valid .mp3 or .wav file")
        except FileNotFoundError as e:
            self.error_diag("Error: Could not play alert sound!", str(e))
        except Exception as e:
            self.error_diag("Error: Could not play alert sound!", str(e))
        play(audio_file)

    def error_diag(self, message, error):
        msg_dialog = QMessageBox()
        msg_dialog.setWindowTitle("Alert sound error")
        msg_dialog.setText(message)
        msg_dialog.setDetailedText(error)
        msg_dialog.setInformativeText(self.configuration.value["alarm_sound"])
        msg_dialog.setStandardButtons(QMessageBox.Ok)
        msg_dialog.setIcon(QMessageBox.Warning)
        msg_dialog.exec_()
