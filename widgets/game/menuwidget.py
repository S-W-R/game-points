from __future__ import annotations

import pickle
import traceback
from pickle import PickleError
from typing import TYPE_CHECKING, Dict

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QMessageBox, \
    QPushButton

from core.gamestate import GameState
from const.paths import SAVE_PATH

if TYPE_CHECKING:
    pass


class MenuWidget(QWidget):
    NUMBERS = 'Zero First Second Third Fourth Fifth Sixth Seventh'.split(' ')

    def __init__(self, game_state: GameState):
        super().__init__()
        self._game_state = game_state
        self.__init_window(game_state)

    def __init_window(self, game_state: GameState):
        layout = QVBoxLayout(self)
        save_button = QPushButton(text='save game')
        save_button.clicked.connect(self.__save_game)
        layout.addWidget(save_button)
        self.player_labels = dict()  # Dict[Player, QLabel]
        for player in game_state.players:
            label = QLabel(text='')
            border_color = player.color_scheme.name
            label.setStyleSheet(f"border: 3px solid {border_color};")
            layout.addWidget(label)
            self.player_labels[player] = label
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    def __save_game(self):
        try:
            with open(SAVE_PATH, 'wb') as file:
                pickle.dump(self._game_state, file)
            QMessageBox.question(self,
                                 'info',
                                 'Saved successfully',
                                 QMessageBox.Yes)
        except Exception as e:
            QMessageBox.question(self,
                                 'Error',
                                 f'Unable to save: \n{e}',
                                 QMessageBox.Yes)

    def paintEvent(self, event):
        for player in self._game_state.players:
            p_adj = self.NUMBERS[player.id]
            p_score = player.score
            label = self.player_labels[player]
            label.setText(f'{p_adj} player: {p_score}')

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
