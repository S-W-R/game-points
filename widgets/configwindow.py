from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QComboBox, QLabel, \
    QGridLayout, QLineEdit, QMessageBox

import const.rules as rules
from core.gamestate import GameState
from geometry.point import Point
from graphic.schemepreset import SchemePreset
from widgets.mainwindow import MainWindow

if TYPE_CHECKING:
    pass


class ConfigWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.__init_window()

    def __init_window(self):
        self.__init_initial_position_combobox()
        self.__init_score_rule_combobox()
        self.__init_start_button()
        layout = QGridLayout(self)
        layout.addWidget(QLabel(text='score rule:'), 0, 0)
        layout.addWidget(self._score_rule_combobox, 0, 1)
        layout.addWidget(QLabel(text='initial position:'), 1, 0)
        layout.addWidget(self._initial_position_combobox, 1, 1)
        layout.addWidget(QLabel(text='Width:'), 2, 0)
        self.width_text = QLineEdit()
        layout.addWidget(self.width_text, 2, 1)
        layout.addWidget(QLabel(text='Height:'), 3, 0)
        self.height_text = QLineEdit()
        layout.addWidget(self.height_text, 3, 1)
        layout.addWidget(self.start_button, 4, 0, 1, 2)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.setWindowTitle("config")
        self.show()

    def __init_score_rule_combobox(self):
        self._score_rule_combobox = QComboBox()
        for i in rules.ScoreRule:
            self._score_rule_combobox.addItem(i.value.name, i)

    def __init_initial_position_combobox(self):
        self._initial_position_combobox = QComboBox()
        for i in rules.InitialPosition:
            self._initial_position_combobox.addItem(i.value.name, i)

    def __init_start_button(self):
        self.start_button = QPushButton(text='start game')
        self.start_button.clicked.connect(self.start_game)

    def start_game(self):
        score_rule = rules.RULE_FROM_NAME[
            self._score_rule_combobox.currentText()]
        initial_pos = rules.RULE_FROM_NAME[
            self._initial_position_combobox.currentText()]
        try:
            width = int(self.width_text.text())
            height = int(self.height_text.text())
        except:
            QMessageBox.critical(self,
                                 "Error",
                                 "Incorrect input",
                                 QMessageBox.Ok)
            return
        if width < 6 or height < 6:
            QMessageBox.critical(self,
                                 "Error",
                                 "Field size must be more then 6x6",
                                 QMessageBox.Ok)
            return
        game_state = GameState(size=Point(width, height),
                               scheme_preset=SchemePreset(),
                               score_rule=score_rule,
                               initial_position=initial_pos)
        self.main_window = MainWindow(game_state)
        self.main_window.show()
        self.close()

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
