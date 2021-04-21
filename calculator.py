import sys
from PyQt5 import uic, Qt

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    win = uic.loadUi("calculator.ui")

    win.show()
    app.exec()
