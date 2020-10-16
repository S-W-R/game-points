from __future__ import annotations

from collections import deque
from queue import Queue
from typing import TYPE_CHECKING, NoReturn, Set, Iterable

from entities.cell import Cell, CellTypes
from entities.player import Player
from geometry.matrix import Matrix
from geometry.point import Point
from graphic.schemepreset import SchemePreset

from itertools import cycle

if TYPE_CHECKING:
    pass


class GameState:
    NEAR_POINTS = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

    def __init__(self, size: Point):
        self._size = size
        self._game_field = self.__init_game_field(size)
        player1 = Player(1, SchemePreset.red.value)
        player2 = Player(2, SchemePreset.blue.value)
        self._empty_player = Player.empty_player()
        self._players = [player1, player2]
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

    def make_turn(self, position: Point) -> NoReturn:
        if not self.is_correct_turn(position):
            return
        cell = self._game_field[position]
        self._activate_cell(self._current_player, cell)
        active_cells = set()  # type:  Set[Point]
        for player in filter(lambda x: x != self._current_player,
                             self._players):
            active_cells.update(self._get_player_active_cells(player))
        free_cells = set()  # type:  Set[Point]
        surrounded_cells = set()  # type:  Set[Point]
        for potential_cell in active_cells:
            if potential_cell in free_cells or potential_cell in surrounded_cells:
                continue
            surrounded = True
            current_group = set()  # type:  Set[Point]
            frontier = deque()
            frontier.append(potential_cell)
            while len(frontier) > 0:
                current = frontier.popleft()
                current_group.add(current)
                if self._is_near_border(current):
                    surrounded = False
                for near_pos in self._get_near_position(current):
                    near_cell = self.game_field[near_pos]
                    if (near_cell.real_owner == self._current_player or
                            near_pos in current_group):
                        continue
                    frontier.append(near_pos)
                    current_group.add(near_pos)
            if surrounded:
                surrounded_cells |= current_group
            else:
                free_cells |= current_group
        self._capture_points(self._current_player, surrounded_cells)
        self._current_player = self._get_next_player()

    def is_correct_turn(self, position: Point):
        if position not in self.game_field:
            return False
        cell_type = self.game_field[position].cell_type
        return cell_type == CellTypes.empty

    def _get_near_position(self, position: Point) -> Iterable[Point]:
        x = position.x
        y = position.y
        for near_pos in self.NEAR_POINTS:
            new_point = position + near_pos
            if new_point in self.game_field:
                yield new_point

    def _is_near_border(self, position: Point) -> bool:
        x = position.x
        y = position.y
        for near_pos in self.NEAR_POINTS:
            new_point = position + near_pos
            if new_point not in self.game_field:
                return True
        return False

    def _get_next_player(self) -> Player:
        return self._player_cycle.__next__()

    def _activate_cell(self, player: Player, cell: Cell):
        cell.real_owner = player
        cell.graphic_owner = player
        cell.cell_type = CellTypes.active_point

    def _capture_points(self, player: Player, points: Iterable[Point]):
        for point in points:
            cell = self.game_field[point]
            if (cell.cell_type == CellTypes.empty or
                    cell.cell_type == CellTypes.captured_cell):
                cell.cell_type = CellTypes.captured_cell
                cell.real_owner = player
                cell.graphic_owner = player
            if (cell.cell_type == CellTypes.active_point or
                    cell.cell_type == CellTypes.inactive_point):
                cell.cell_type = CellTypes.inactive_point
                cell.real_owner = player
            if (cell.cell_type == CellTypes.inactive_point and
                    cell.graphic_owner == cell.real_owner):
                cell.cell_type = CellTypes.active_point

    def _get_player_active_cells(self, player: Player) -> Iterable[Point]:
        for x in range(self.game_field.width):
            for y in range(self.game_field.height):
                cell = self.game_field[Point(x, y)]
                if cell.real_owner == player and cell.cell_type == CellTypes.active_point:
                    yield cell.position
