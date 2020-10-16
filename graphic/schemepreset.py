from enum import Enum

from PyQt5.QtGui import QColor

from entities.cell import CellTypes
from graphic.cellgraphic import CellGraphic
from graphic.colorscheme import ColorScheme

SIZE_EMPTY = 0.3
SIZE_ACTIVE = 0.5
SIZE_INACTIVE = 0.46
SIZE_CAPTURED = 0.35


class SchemePreset(Enum):
    empty = ColorScheme(
        {CellTypes.empty: CellGraphic(SIZE_EMPTY,
                                      QColor(255, 255, 255, 30)),
         CellTypes.active_point: CellGraphic(SIZE_ACTIVE,
                                             QColor(255, 255, 255, 50)),
         CellTypes.inactive_point: CellGraphic(SIZE_INACTIVE,
                                               QColor(200, 200, 200, 50)),
         CellTypes.captured_cell: CellGraphic(SIZE_CAPTURED,
                                              QColor(180, 180, 180, 80))})
    red = ColorScheme(
        {CellTypes.empty: CellGraphic(SIZE_EMPTY,
                                      QColor(255, 0, 0, 30)),
         CellTypes.active_point: CellGraphic(SIZE_ACTIVE,
                                             QColor(255, 0, 0, 255)),
         CellTypes.inactive_point: CellGraphic(SIZE_INACTIVE,
                                               QColor(210, 30, 30, 200)),
         CellTypes.captured_cell: CellGraphic(SIZE_CAPTURED,
                                              QColor(200, 100, 100, 80))})
    blue = ColorScheme(
        {CellTypes.empty: CellGraphic(SIZE_EMPTY,
                                      QColor(0, 0, 255, 30)),
         CellTypes.active_point: CellGraphic(SIZE_ACTIVE,
                                             QColor(0, 0, 255, 255)),
         CellTypes.inactive_point: CellGraphic(SIZE_INACTIVE,
                                               QColor(30, 30, 210, 200)),
         CellTypes.captured_cell: CellGraphic(SIZE_CAPTURED,
                                              QColor(100, 100, 200, 80))})
