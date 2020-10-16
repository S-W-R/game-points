from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt, QPointF
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QPainter, QTransform, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QWidget

from gamewindow import GameWindow
from geometry.point import Point

if TYPE_CHECKING:
    from gamestate import GameState


class MainWindow(QWidget):

    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.__init_window(game_state)

    def __init_window(self, game_state: GameState):

        layout = QHBoxLayout(self)
        self.game_widget = GameWindow(self.game_state)
        layout.addWidget(self.game_widget)
        layout.addWidget(QPushButton('PyQt5 button1'))
        layout.setStretch(0, 10)
        layout.setStretch(1, 0)
        self.setLayout(layout)
        self.setWindowTitle("Points")
        #self.setMinimumSize(GameWindow.min_size())
        self.show()



    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()