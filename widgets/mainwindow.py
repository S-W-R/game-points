from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from const import rules
from widgets.game.gamewidget import GameWindow
from widgets.game.menuwidget import MenuWidget

if TYPE_CHECKING:
    from core.gamestate import GameState


class MainWindow(QWidget):
    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.__init_window(game_state)

    def __init_window(self, game_state: GameState):
        layout = QHBoxLayout(self)
        self.game_widget = GameWindow(game_state)
        self.menu_widget = MenuWidget(game_state)
        layout.addWidget(self.game_widget)
        layout.addWidget(self.menu_widget)
        layout.setStretch(0, 10)
        layout.setStretch(1, 0)
        self.setLayout(layout)
        self.setWindowTitle("Points")
        # self.setMinimumSize(GameWindow.min_size())
        self.__init_timer()
        self.show()

    def __init_timer(self):
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_state)
        self.game_timer.start(100)

    def update_game_state(self):
        if self.game_state.current_state == rules.CurrentState.ai_playing:
            self.game_state.ai_make_turn()
        elif self.game_state.current_state == rules.CurrentState.ended:
            self.setWindowTitle('Points: game over')
            self.game_timer.stop()

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
