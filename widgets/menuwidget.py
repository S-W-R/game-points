from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from core.gamestate import GameState

if TYPE_CHECKING:
    pass


class MenuWidget(QWidget):

    def __init__(self, game_state: GameState):
        super().__init__()
        self._game_state = game_state
        self.__init_window()

    def __init_window(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(text='scores:'))
        self.first_player_score = QLabel(text='')
        self.second_player_score = QLabel(text='')
        layout.addWidget(self.first_player_score)
        layout.addWidget(self.second_player_score)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.show()

    def paintEvent(self, event):
        first_score = self._game_state.get_player_score(
            self._game_state.get_player_by_id(1))
        self.first_player_score.setText(f'First player: {first_score}')
        second_score = self._game_state.get_player_score(
            self._game_state.get_player_by_id(2))
        self.second_player_score.setText(f'Second player: {second_score}')


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
