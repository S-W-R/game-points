from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QComboBox, QLabel, \
    QGridLayout, QMessageBox

import const.rules as rules
from const.paths import SAVE_PATH
from core.gamestate import GameState
from geometry.point import Point
from graphic.schemepreset import SchemePreset
from widgets.config.playersconfig import PlayersConfig
from widgets.config.valueslider import ValueSlider
from widgets.mainwindow import MainWindow
import pickle

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
        self._initial_position_combobox = \
            self.__create_initial_position_combobox()
        self._score_rule_combobox = self.__create_score_rule_combobox()

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
        start_button = self.__create_start_button()
        load_button = self.__create_load_button()
        layout.addWidget(start_button, 5, 0, 1, 2)
        layout.addWidget(load_button, 6, 0, 1, 2)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setWindowTitle("points game config")
        self.show()

    def __create_score_rule_combobox(self):
        score_rule_combobox = QComboBox()
        for i in rules.ScoreRule:
            score_rule_combobox.addItem(i.value.name, i)
        return score_rule_combobox

    def __create_initial_position_combobox(self):
        initial_position_combobox = QComboBox()
        for i in rules.InitialPosition:
            initial_position_combobox.addItem(i.value.name, i)
        return initial_position_combobox

    def __create_start_button(self):
        start_button = QPushButton(text='start game')
        start_button.clicked.connect(self.__start_game)
        return start_button

    def __create_load_button(self):
        load_button = QPushButton(text='load game')
        load_button.clicked.connect(self.__load_game)
        return load_button

    def __star_game_window(self, game_state: GameState):
        self.main_window = MainWindow(game_state)
        self.main_window.show()
        self.close()

    def __load_game(self):
        if not SAVE_PATH.is_file():
            QMessageBox.question(self,
                                 'Error',
                                 'Save file not found or not created',
                                 QMessageBox.Yes)
            return
        try:
            with open(SAVE_PATH, 'rb') as file:
                game_state = pickle.load(file)
            QMessageBox.question(self,
                                 'info',
                                 'Loaded successfully',
                                 QMessageBox.Yes)
            self.__star_game_window(game_state)
        except Exception as e:
            QMessageBox.question(self,
                                 'Error',
                                 f'Unable to load: \n{e}',
                                 QMessageBox.Yes)

    def __start_game(self):
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
