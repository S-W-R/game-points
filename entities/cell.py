from __future__ import annotations
from typing import NoReturn

from entities.celltypes import CellTypes
from entities.player import Player
from geometry.point import Point


class Cell:
    def __init__(self, position: Point, cell_type: CellTypes, owner: Player):
        self._position = position
        self._cell_type = cell_type
        self._owner = owner

    @staticmethod
    def create_empty_cell(position: Point) -> Cell:
        return Cell(position, CellTypes.empty, Player.empty_player())

    @property
    def position(self) -> Point:
        return self._position

    @property
    def cell_type(self) -> CellTypes:
        return self._cell_type

    @cell_type.setter
    def cell_type(self, value: CellTypes) -> NoReturn:
        self._cell_type = value

    @property
    def owner(self) -> Player:
        return self._owner

    @owner.setter
    def owner(self, value: Player) -> NoReturn:
        self._owner = value
