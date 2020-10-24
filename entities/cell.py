from __future__ import annotations
from typing import NoReturn, TYPE_CHECKING
from entities.celltype import CellType

if TYPE_CHECKING:
    from geometry.point import Point
    from entities.player import Player


class Cell:
    def __init__(self, position: Point, cell_type: CellType, owner: Player):
        self._position = position
        self._cell_type = cell_type
        self._owner = owner
        self._graphic_owner = owner

    @staticmethod
    def create_empty_cell(position: Point) -> Cell:
        return Cell(position, CellType.empty, Player.empty_player())

    @property
    def position(self) -> Point:
        return self._position

    @property
    def cell_type(self) -> CellType:
        return self._cell_type

    @cell_type.setter
    def cell_type(self, value: CellType) -> NoReturn:
        self._cell_type = value

    @property
    def real_owner(self) -> Player:
        return self._owner

    @real_owner.setter
    def real_owner(self, value: Player) -> NoReturn:
        self._owner = value

    @property
    def graphic_owner(self) -> Player:
        return self._graphic_owner

    @graphic_owner.setter
    def graphic_owner(self, value: Player) -> NoReturn:
        self._graphic_owner = value
