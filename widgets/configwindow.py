from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QComboBox, QLabel, \
    QGridLayout

import const.rules as rules
from core.gamestate import GameState
from entities.player import Player
from geometry.point import Point
from graphic.schemepreset import SchemePreset
from widgets.config.playeredit import PlayerEditor
from widgets.config.playersconfig import PlayersConfig
from widgets.config.valueslider import ValueSlider
from widgets.mainwindow import MainWindow

if TYPE_CHECKING:
    pass


class ConfigWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.__init_window()

    def __init_game_parameters(self):
        self.rule_score = rules.ScoreRule.russian
        self.rule_initial_pos = rules.InitialPosition.cross
        self.game_width = 10
        self.game_height = 10

    def __init_window(self):
        self.__init_initial_position_combobox()
        self.__init_score_rule_combobox()
        self.__init_start_button()
        schemes = SchemePreset()
        layout = QGridLayout(self)
        layout.addWidget(QLabel(text='score rule:'), 0, 0)
        layout.addWidget(self._score_rule_combobox, 0, 1)
        layout.addWidget(QLabel(text='initial position:'), 1, 0)
        layout.addWidget(self._initial_position_combobox, 1, 1)
        layout.addWidget(QLabel(text='Width:'), 2, 0)
        self.width_slider = ValueSlider(10, 50)
        layout.addWidget(self.width_slider, 2, 1)
        layout.addWidget(QLabel(text='Height:'), 3, 0)
        self.height_slider = ValueSlider(10, 30)
        layout.addWidget(self.height_slider, 3, 1)
        self.players_config = PlayersConfig(2, len(schemes), schemes)
        layout.addWidget(self.players_config, 4, 0, 1, 2)
        layout.addWidget(self.start_button, 5, 0, 1, 2)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setWindowTitle("points game config")
        self.show()

    def __init_score_rule_combobox(self):
        self._score_rule_combobox = QComboBox()
        for i in rules.ScoreRule:
            self._score_rule_combobox.addItem(i.value.name, i)
        return self._score_rule_combobox

    def __init_initial_position_combobox(self):
        self._initial_position_combobox = QComboBox()
        for i in rules.InitialPosition:
            self._initial_position_combobox.addItem(i.value.name, i)
        return self._initial_position_combobox

    def __init_start_button(self):
        self.start_button = QPushButton(text='start game')
        self.start_button.clicked.connect(self.start_game)
        return self.start_button

    def __star_game_window(self, game_state: GameState):
        self.main_window = MainWindow(game_state)
        self.main_window.show()
        self.close()

    def start_game(self):
        score_rule = rules.SCORE_RULE_FROM_NAME[
            self._score_rule_combobox.currentText()]
        initial_pos = rules.INITIAL_POSITION_FROM_RULE[
            self._initial_position_combobox.currentText()]
        width = self.width_slider.value
        height = self.height_slider.value
        players = self.players_config.get_players()
        game_state = GameState(size=Point(width, height),
                               score_rule=score_rule,
                               initial_position=initial_pos,
                               players=players)
        self.__star_game_window(game_state)

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
