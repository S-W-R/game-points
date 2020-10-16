from enum import Enum

from PyQt5.QtGui import QColor

from entities.cell import CellTypes
from graphic.cellgraphic import CellGraphic
from graphic.colorscheme import ColorScheme


class SchemePreset(Enum):
    empty = ColorScheme(
        {CellTypes.empty: CellGraphic(0.3, QColor(255, 255, 255, 30)),
         CellTypes.active_point: CellGraphic(0.5, QColor(255, 255, 255, 50)),
         CellTypes.inactive_point: CellGraphic(0.4,
                                               QColor(255, 255, 200, 50))})
    red = ColorScheme(
        {CellTypes.empty: CellGraphic(0.25, QColor(255, 0, 0, 30)),
         CellTypes.active_point: CellGraphic(0.5, QColor(255, 0, 0, 255)),
         CellTypes.inactive_point: CellGraphic(0.4, QColor(200, 0, 0, 255))})
    blue = ColorScheme(
        {CellTypes.empty: CellGraphic(0.25, QColor(0, 0, 255, 30)),
         CellTypes.active_point: CellGraphic(0.5, QColor(0, 0, 255, 255)),
         CellTypes.inactive_point: CellGraphic(0.4, QColor(0, 0, 200, 255))})
