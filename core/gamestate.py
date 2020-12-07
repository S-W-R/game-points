from __future__ import annotations

import itertools
from collections import deque
from typing import TYPE_CHECKING, Set, Iterable, List, NoReturn

import const.rules as rules
from core.gamehelper import GameHelper
from entities.cell import Cell
from entities.celltype import CellType
from entities.player import Player
from geometry.matrix import Matrix
from geometry.point import Point

if TYPE_CHECKING:
    pass


class GameState:
    NEAR_POINTS = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

    def __init__(self, size: Point,
                 score_rule: rules.ScoreRule,
                 initial_position: rules.InitialPosition,
                 players: Iterable[Player]):
        self.score_rule = score_rule.value.name
        self._size = size
        self._empty_player = Player.empty_player()
        self._players = list(players)
        self._player_cycle = itertools.cycle(self._players)
        self._current_player = self._get_next_player()
        self._game_field = self.__init_game_field(size)
        self.__apply_initial_position(initial_position)
        self._game_helper = GameHelper(self)
        self._current_state = rules.CurrentState.player_playing
        self._current_state = self._get_current_state()

    def __init_game_field(self, size: Point) -> Matrix[Cell]:
        game_field = Matrix.from_point(size)
        for x in range(game_field.width):
            for y in range(game_field.height):
                point = Point(x, y)
                game_field[point] = Cell.create_empty_cell(point)
        return game_field

    def __apply_initial_position(self,
                                 initial_position: rules.InitialPosition):
        first_player_pos = ()
        second_player_pos = ()
        central_pos = Point(0, 0)
        if initial_position == rules.InitialPosition.empty:
            pass
        elif initial_position == rules.InitialPosition.cross:
            if len(self._players) != 2:
                raise AttributeError()
            first_player_pos = (Point(0, 0), Point(1, 1))
            second_player_pos = (Point(0, 1), Point(1, 0))
            central_pos = Point(self.width // 2 - 1, self.height // 2 - 1)
        elif initial_position == rules.InitialPosition.double_cross:
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
    def game_helper(self) -> GameHelper:
        return self._game_helper

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def empty_player(self) -> Player:
        return self._empty_player

    @property
    def current_player(self) -> Player:
        return self.current_player

    @property
    def current_state(self) -> rules.CurrentState:
        return self._current_state

    @property
    def size(self) -> Point:
        return self._size

    @property
    def height(self) -> int:
        return self._size.y

    @property
    def width(self) -> int:
        return self._size.x

    def get_near_position(self, position: Point) -> Iterable[Point]:
        for near_pos in self.NEAR_POINTS:
            new_point = position + near_pos
            if new_point in self.game_field:
                yield new_point

    def ai_make_turn(self):
        player = self._current_player
        controller = player.controller
        position_to_move = controller.get_position(self, player)
        self.make_turn(position=position_to_move, player=player)
        self._update_turn_is_end()

    def player_make_turn(self, position: Point):
        if (self.try_make_turn(position, self._current_player) and
                self._current_state == rules.CurrentState.player_playing):
            self._update_turn_is_end()

    def _update_turn_is_end(self):
        for player in self._players:
            player.score = self._get_player_score(player)
        self._current_player = self._get_next_player()
        self._current_state = self._get_current_state()

    def _get_current_state(self):
        if not self.game_helper.is_player_can_make_turn(self._current_player):
            return rules.CurrentState.ended
        else:
            if self._current_player.controller.is_ai:
                return rules.CurrentState.ai_playing
            else:
                return rules.CurrentState.player_playing

    def try_make_turn(self, position: Point, player: Player) -> bool:
        if not self.is_correct_turn(position, player):
            return False
        self.make_turn(position, player)
        return True

    def make_turn(self, position: Point, player: Player) -> NoReturn:
        if not self.is_correct_turn(position, player):
            raise Exception('incorrect turn')
        cell = self._game_field[position]
        self._activate_cell(player, cell)
        active_cells = set(
            self.game_helper.get_enemy_positions(player))
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
                for near_pos in self.get_near_position(current):
                    near_cell = self.game_field[near_pos]
                    if (near_cell.real_owner == player or
                            near_pos in current_group):
                        continue
                    frontier.append(near_pos)
                    current_group.add(near_pos)
            if surrounded:
                surrounded_cells |= current_group
            else:
                free_cells |= current_group
        self._capture_points(player, surrounded_cells)

    def is_correct_turn(self, position: Point, player: Player):
        if position not in self.game_field:
            return False
        cell = self.game_field[position]
        cell_type = cell.cell_type
        owner = cell.real_owner
        return (cell_type == CellType.empty or (
                cell_type == CellType.captured_cell and owner == player))

    def _get_player_score(self, player: Player) -> int:
        counter = 0
        score_rule = rules.SCORE_RULE_FROM_NAME[self.score_rule]
        if score_rule == rules.ScoreRule.russian:
            for cell in self.game_helper.get_player_cells(player):
                if cell.cell_type == CellType.inactive_point:
                    counter += 1
        elif score_rule == rules.ScoreRule.polish:
            for cell in self.game_helper.get_player_cells(player):
                if cell.cell_type == CellType.inactive_point:
                    counter += 2
                elif cell.cell_type == CellType.captured_cell:
                    counter += 1
        else:
            raise AttributeError()
        return counter

    def get_player_by_id(self, player_id: int) -> Player:
        return self._players[player_id - 1]

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
