from PyQt5.QtWidgets import QApplication
import sys

from graphic.schemepreset import SchemePreset
from widgets.mainwindow import MainWindow
from core.gamestate import GameState
from geometry.point import Point

if __name__ == "__main__":
    game_state_test = GameState(size=Point(20, 20),
                                scheme_preset=SchemePreset())
    App = QApplication(sys.argv)
    window = MainWindow(game_state_test)
    sys.exit(App.exec())
