from PyQt5.QtWidgets import QApplication
import sys

from graphic.schemepreset import SchemePreset
from widgets.configwindow import ConfigWindow
from widgets.mainwindow import MainWindow
from core.gamestate import GameState
from geometry.point import Point
import const.rules as rules

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = ConfigWindow()
    sys.exit(App.exec())
