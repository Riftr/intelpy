from PyQt5.QtCore import pyqtSignal, QObject


class EveworkerSignals(QObject):
    message_ready = pyqtSignal(list)
