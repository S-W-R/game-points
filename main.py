from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys

from gamewindow import GameWindow
from mainwindow import MainWindow
from gamestate import GameState
from geometry.point import Point

if __name__ == "__main__":
    game_state_test = GameState(size=Point(10, 10))
    App = QApplication(sys.argv)
    window = MainWindow(game_state_test)
    sys.exit(App.exec())
