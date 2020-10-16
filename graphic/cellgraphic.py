from PyQt5.QtGui import QColor


class CellGraphic:
    def __init__(self, size: float, color: QColor):
        self._size = size
        self._color = color

    @property
    def size(self) -> float:
        return self._size

    @property
    def color(self) -> QColor:
        return self._color
