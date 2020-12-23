import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from widgets.configwindow import ConfigWindow


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QtWidgets.QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncaught_exceptions

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = ConfigWindow()
    sys.exit(App.exec())
