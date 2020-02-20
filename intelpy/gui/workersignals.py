import traceback, sys
from PyQt5.QtCore import *

class WorkerSignals(QObject):

    new_chatlog_line = pyqtSignal(object)
    error = pyqtSignal(tuple)
