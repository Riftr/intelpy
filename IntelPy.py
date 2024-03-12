# entry point script for pyinstaller
from intelpy.__main__ import main as mymain
import PyQt5
from PyQt5 import QtWidgets

if __name__ == '__main__':
    try:
        mymain()
    except Exception as e:
        print("IntelPy ended with an error: \n" + str(e))
        #pop up gui error msg
        app = QtWidgets.QApplication([])
        error_diag = QtWidgets.QErrorMessage()
        error_diag.setWindowTitle("IntelPy Error")
        error_diag.showMessage('IntelPy ended with an error: \n ' + str(e))
        app.exec_()
        raise
