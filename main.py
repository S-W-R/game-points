import sys

from PyQt5.QtWidgets import QApplication

from widgets.configwindow import ConfigWindow

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = ConfigWindow()
    sys.exit(App.exec())
