from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, NoReturn, Set, Iterable

import const.rules as rules
from entities.cell import Cell
from entities.celltype import CellType
from entities.player import Player
from geometry.matrix import Matrix
from geometry.point import Point
from graphic.schemepreset import SchemePreset

import itertools

if TYPE_CHECKING:
    pass


class GameState:
    NEAR_POINTS = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

    def __init__(self, size: Point, scheme_preset: SchemePreset,
                 score_rule: rules.ScoreRule,
                 initial_position: rules.InitialPosition):
        self.__init_rules(score_rule, initial_position)
        self._size = size
        player1 = Player(1, scheme_preset['red'])
        player2 = Player(2, scheme_preset['blue'])
        self._empty_player = Player.empty_player()
        self._players = [player1, player2]
        self._player_cycle = itertools.cycle([player1, player2])
        self._current_player = self._get_next_player()
        self._game_field = self.__init_game_field(size)
        self.__apply_initial_position()

    def __init_rules(self, score_rule: rules.ScoreRule,
                     initial_position: rules.InitialPosition):
        self.rule_score = score_rule
        self.rule_initial_position = initial_position

    def __init_game_field(self, size: Point) -> Matrix[Cell]:
        game_field = Matrix.from_point(size)
        for x in range(game_field.width):
            for y in range(game_field.height):
                point = Point(x, y)
                game_field[point] = Cell.create_empty_cell(point)
        return game_field

    def __apply_initial_position(self):
        first_player_pos = ()
        second_player_pos = ()
        central_pos = Point(0, 0)
        if self.rule_initial_position == rules.InitialPosition.empty:
            pass
        elif self.rule_initial_position == rules.InitialPosition.cross:
            if len(self._players) != 2:
                raise AttributeError()
            first_player_pos = (Point(0, 0), Point(1, 1))
            second_player_pos = (Point(0, 1), Point(1, 0))
            central_pos = Point(self.width // 2 - 1, self.height // 2 - 1)
        elif self.rule_initial_position == rules.InitialPosition.double_cross:
            if len(self._players) != 2:
                raise AttributeError()
            first_player_pos = (
                Point(0, 0), Point(1, 1), Point(2, 1), Point(3, 0))
            second_player_pos = (
                Point(0, 1), Point(1, 0), Point(2, 0), Point(3, 1))
            central_pos = Point(self.width // 2 - 2, self.height // 2 - 1)
        else:
            raise AttributeError()
        for i in first_player_pos:
            self._activate_cell(self._players[0],
                                self.game_field[central_pos + i])
        for i in second_player_pos:
            self._activate_cell(self._players[1],
                                self.game_field[central_pos + i])

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
        active_cells = set(
            self._get_enemy_cells(self._current_player))  # type:  Set[Point]
        free_cells = set()  # type:  Set[Point]
        surrounded_cells = set()  # type:  Set[Point]
        for potential_cell in active_cells:
            if potential_cell in free_cells | surrounded_cells:
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
        return cell_type == CellType.empty

    def get_player_score(self, player: Player) -> int:
        counter = 0
        if self.rule_score == rules.ScoreRule.russian:
            for cell in self._get_player_cells(player):
                if cell.cell_type == CellType.inactive_point:
                    counter += 1
        elif self.rule_score == rules.ScoreRule.polish:
            for cell in self._get_player_cells(player):
                if cell.cell_type == CellType.inactive_point:
                    counter += 2
                elif cell.cell_type == CellType.captured_cell:
                    counter += 1
        else:
            raise AttributeError()
        return counter

    def get_player_by_id(self, player_id: int) -> Player:
        return self._players[player_id - 1]

    def _get_near_position(self, position: Point) -> Iterable[Point]:
        for near_pos in self.NEAR_POINTS:
            new_point = position + near_pos
            if new_point in self.game_field:
                yield new_point

    def _is_near_border(self, position: Point) -> bool:
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
        cell.cell_type = CellType.active_point

    def _capture_points(self, player: Player, points: Iterable[Point]):
        for point in points:
            cell = self.game_field[point]
            if (cell.cell_type == CellType.empty or
                    cell.cell_type == CellType.captured_cell):
                cell.cell_type = CellType.captured_cell
                cell.real_owner = player
                cell.graphic_owner = player
            if (cell.cell_type == CellType.active_point or
                    cell.cell_type == CellType.inactive_point):
                cell.cell_type = CellType.inactive_point
                cell.real_owner = player
            if (cell.cell_type == CellType.inactive_point and
                    cell.graphic_owner == cell.real_owner):
                cell.cell_type = CellType.active_point

    def _get_player_active_cells(self, player: Player) -> Iterable[Point]:
        for cell in self._get_player_cells(player):
            if cell.cell_type == CellType.active_point:
                yield cell.position

    def _get_enemy_cells(self, player: Player) -> Iterable[Point]:
        for enemy in itertools.chain((self._empty_player,), self._players):
            if enemy == player:
                continue
            for cell in self._get_player_cells(enemy):
                yield cell.position

    def _get_player_cells(self, player: Player) -> Iterable[Cell]:
        for x in range(self.game_field.width):
            for y in range(self.game_field.height):
                cell = self.game_field[Point(x, y)]
                if cell.real_owner == player:
                    yield cell
