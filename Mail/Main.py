from PyQt5.QtWidgets import QApplication
from Login import Login
import sys


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())