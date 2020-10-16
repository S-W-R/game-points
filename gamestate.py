from __future__ import annotations

from typing import TYPE_CHECKING

from entities.cell import Cell, CellTypes
from entities.player import Player
from geometry.matrix import Matrix
from geometry.point import Point
from graphic.schemepreset import SchemePreset

from itertools import cycle

if TYPE_CHECKING:
    pass


class GameState:
    def __init__(self, size: Point):
        self._size = size
        self._game_field = self.__init_game_field(size)
        player1 = Player(1, SchemePreset.red.value)
        player2 = Player(1, SchemePreset.blue.value)
        self._players = [Player.empty_player(), player1, player2]
        self._player_cycle = cycle([player1, player2])
        self._current_player = self._get_next_player()

    @staticmethod
    def __init_game_field(size: Point) -> Matrix[Cell]:
        game_field = Matrix.from_point(size)
        for x in range(game_field.width):
            for y in range(game_field.height):
                point = Point(x, y)
                game_field[point] = Cell.create_empty_cell(point)
        return game_field

    @property
    def game_field(self) -> Matrix[Cell]:
        return self._game_field

    @property
    def size(self) -> Point:
        return self._size

    @property
    def height(self) -> int:
        return self._size.y

    @property
    def width(self) -> int:
        return self._size.x

    def make_turn(self, position: Point):
        cell = self._game_field[position]
        cell.owner = self._current_player
        cell.cell_type = CellTypes.active_point
        self._current_player = self._get_next_player()

    def _get_next_player(self) -> Player:
        return self._player_cycle.__next__()
