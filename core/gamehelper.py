from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Iterable

import const.rules as rules
from entities.cell import Cell
from entities.celltype import CellType
from entities.player import Player
from geometry.point import Point

if TYPE_CHECKING:
    from core.gameinfo import GameInfo


class GameHelper:
    def __init__(self, game_state: GameInfo):
        self.game_state = game_state

    def get_player_active_cells(self, player: Player) -> Iterable[Point]:
        for cell in self.get_player_cells(player):
            if cell.cell_type == CellType.active_point:
                yield cell.position

    def get_enemy_positions(self, player: Player) -> Iterable[Point]:
        empty_player = self.game_state.empty_player
        players = self.game_state.players
        for enemy in itertools.chain((empty_player,), players):
            if enemy == player:
                continue
            for cell in self.get_player_cells(enemy):
                yield cell.position

    DIAGONAL_POINTS = (Point(-1, -1), Point(-1, 1), Point(1, -1), Point(1, 1))

    def get_diagonal_points(self, position: Point):
        for near_pos in self.DIAGONAL_POINTS:
            new_point = position + near_pos
            if new_point in self.game_state.game_field:
                yield new_point

    def is_enemy_or_neutral_point(self, point: Point, player: Player) -> bool:
        return not self.is_ally_point(point, player)

    def is_enemy_point(self, point: Point, player: Player) -> bool:
        return (not self.is_neutral_point(point) and
                self.is_enemy_or_neutral_point(point, player))

    def is_neutral_point(self, point: Point):
        cell = self.game_state.game_field[point]
        return cell.real_owner == self.game_state.empty_player

    def is_ally_point(self, point: Point, player: Player) -> bool:
        cell = self.game_state.game_field[point]
        return cell.real_owner == player

    def get_player_cells(self, player: Player) -> Iterable[Cell]:
        for cell in self.get_game_cells():
            if cell.real_owner == player:
                yield cell

    def get_available_positions(self, player: Player) -> Iterable[Point]:
        for cell in self.get_game_cells():
            if self.game_state.is_correct_turn(cell.position, player):
                yield cell.position

    def get_available_neutral_positions(self,
                                        player: Player) -> Iterable[Point]:
        for cell in self.get_game_cells():
            if (self.game_state.is_correct_turn(cell.position, player) and
                    not self.is_ally_point(cell.position, player)):
                yield cell.position

    def get_game_cells(self) -> Iterable[Cell]:
        game_field = self.game_state.game_field
        for x in range(game_field.width):
            for y in range(game_field.height):
                yield self.game_state.game_field[Point(x, y)]

    def is_player_can_make_turn(self, player: Player):
        if self.game_state.current_state == rules.CurrentState.ended:
            return False
        for point in self.get_available_positions(player):
            return True
        return False

    def is_game_ended(self, player: Player):
        if self.game_state.current_state == rules.CurrentState.ended:
            return True
        for point in self.get_available_neutral_positions(player):
            return True
        return False
