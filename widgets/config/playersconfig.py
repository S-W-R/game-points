from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout

from graphic.schemepreset import SchemePreset
from widgets.config.playerlayout import PlayersLayout

if TYPE_CHECKING:
    pass


class PlayersConfig(QWidget):
    def __init__(self, min_count: int, max_count: int, scheme: SchemePreset):
        super().__init__()
        self._min_count = min_count
        self._max_count = max_count
        self.schemes = scheme
        main_layout = QGridLayout(self)
        self._add_player_button = self.__init_add_player_button()
        self._remove_player_button = self.__init_remove_player_button()
        self.player_layout = PlayersLayout(scheme)
        main_layout.addWidget(self._add_player_button, 0, 0)
        main_layout.addWidget(self._remove_player_button, 0, 1)
        main_layout.addWidget(self.player_layout, 1, 0, 1, 2)
        main_layout.setAlignment(Qt.AlignTop)
        while self.player_layout.players_count < self._min_count:
            self.add_player()
        self.setLayout(main_layout)
        self.show()
        self.update()

    def __init_add_player_button(self):
        add_player_button = QPushButton(text='add player')
        add_player_button.clicked.connect(self.add_player)
        return add_player_button

    def __init_remove_player_button(self):
        remove_player_button = QPushButton(text='remove player')
        remove_player_button.clicked.connect(self.remove_player)
        return remove_player_button

    def add_player(self):
        if self.player_layout.players_count >= self._max_count:
            return
        self.player_layout.add_player()

    def remove_player(self):
        if self.player_layout.players_count <= self._min_count:
            return
        self.player_layout.remove_player()

    def get_players(self):
        return self.player_layout.get_players()

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
