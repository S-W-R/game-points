from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel

from const import rules, controllers
from entities.player import Player
from graphic.schemepreset import SchemePreset

if TYPE_CHECKING:
    pass


class PlayerEditor(QWidget):
    def __init__(self, player_id: int, initial_index: int,
                 schemes: SchemePreset):
        super().__init__()
        self._player_id = player_id
        self._schemes = schemes
        self._controller_type_combobox = self.__create_controller_combobox()
        self._scheme_combobox = self.__create_scheme_combobox(schemes,
                                                              initial_index)
        layout = QGridLayout(self)
        layout.addWidget(QLabel(text=f'Player {player_id} configuration:'),
                         0, 0, 1, 2)
        layout.addWidget(QLabel(text='controller:'), 1, 0)
        layout.addWidget(self._controller_type_combobox, 1, 1)
        layout.addWidget(QLabel(text='color:'), 2, 0)
        layout.addWidget(self._scheme_combobox, 2, 1)
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 10)
        self.setLayout(layout)
        self.update()

    def __create_controller_combobox(self) -> QComboBox:
        controller_type_combobox = QComboBox()
        for i in controllers.ControllerType:
            controller_type_combobox.addItem(i.value.name, i)
        return controller_type_combobox

    def __create_scheme_combobox(self, schemes: SchemePreset,
                                 initial_index: int) -> QComboBox:
        scheme_combobox = QComboBox()
        for i in schemes:
            scheme_combobox.addItem(i.name, i)
        scheme_combobox.setCurrentIndex(initial_index)
        return scheme_combobox

    def create_player(self):
        controller_type = controllers.CONTROLLER_FROM_NAME[
            self._controller_type_combobox.currentText()]
        scheme_name = self._scheme_combobox.currentText()
        scheme = self._schemes[scheme_name]
        return Player(player_id=self._player_id,
                      color_scheme=scheme,
                      controller=controller_type)

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
