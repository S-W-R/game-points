from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt5 import QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QSlider, QLabel

if TYPE_CHECKING:
    pass


class ValueSlider(QWidget):

    def __init__(self, min_value: int, max_value: int):
        super().__init__()
        self._min_value = min_value
        self._max_value = max_value
        self._current_value = self._min_value
        layout = QHBoxLayout(self)
        self._label = QLabel('')
        self._slider = self.__create_slider(min_value, max_value)
        self._slider.valueChanged.connect(self._update_value)
        layout.addWidget(self._slider)
        layout.addWidget(self._label)
        layout.setStretch(0, 10)
        layout.setStretch(1, 0)
        self.setLayout(layout)
        self.setWindowTitle("Points")

    def __create_slider(self, min_value: int, max_value: int) -> QSlider:
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setMinimumWidth((max_value - min_value) * 12)
        return slider

    def _update_value(self, value):
        self._current_value = value
        self._update_label(self._current_value)

    def _update_label(self, value):
        self._label.setText(str(value))

    @property
    def min_value(self) -> int:
        return self._min_value

    @property
    def max_value(self) -> int:
        return self._max_value

    @property
    def value(self) -> int:
        return self._current_value

    def paintEvent(self, event):
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()
