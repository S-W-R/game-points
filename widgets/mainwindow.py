from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from widgets.gamewidget import GameWindow

if TYPE_CHECKING:
    from core.gamestate import GameState


class MainWindow(QWidget):

    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.__init_window(game_state)

    def __init_window(self, game_state: GameState):
        layout = QHBoxLayout(self)
        self.game_widget = GameWindow(self.game_state)
        layout.addWidget(self.game_widget)
        layout.addWidget(QPushButton('Place for UI widget'))
        layout.setStretch(0, 10)
        layout.setStretch(1, 0)
        self.setLayout(layout)
        self.setWindowTitle("Points")
        # self.setMinimumSize(GameWindow.min_size())
        self.show()

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
