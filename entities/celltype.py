from enum import Enum, auto


class CellType(Enum):
    empty = auto()
    active_point = auto()
    inactive_point = auto()
    captured_cell = auto()
