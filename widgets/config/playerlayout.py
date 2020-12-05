from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QHBoxLayout, QWidget

from graphic.schemepreset import SchemePreset
from widgets.config.playeredit import PlayerEditor

if TYPE_CHECKING:
    pass


class PlayersLayout(QWidget):
    def __init__(self, scheme: SchemePreset):
        super().__init__()
        self.scheme = scheme
        self.player_editors = []  # List[PlayerEditor]
        self._player_layout = QHBoxLayout(self)
        self.setLayout(self._player_layout)

    @property
    def players_count(self):
        return len(self.player_editors)

    def add_player(self):
        new_player_id = self.get_next_player_id()
        new_player_scheme_index = self.get_next_player_scheme_index()
        player_editor = PlayerEditor(player_id=new_player_id,
                                     initial_index=new_player_scheme_index,
                                     schemes=self.scheme)
        self.player_editors.append(player_editor)
        self._player_layout.addWidget(player_editor)

    def remove_player(self):
        item = self.player_editors.pop()
        self._player_layout.removeWidget(item)
        item.close()

    def get_next_player_id(self):
        return len(self.player_editors) + 1

    def get_next_player_scheme_index(self):
        return len(self.player_editors)

    def get_players(self):
        return [i.create_player() for i in self.player_editors]
