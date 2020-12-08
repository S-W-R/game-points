from __future__ import annotations

from typing import TYPE_CHECKING, Iterable
from controllers.controller import Controller
from geometry.point import Point
import random

if TYPE_CHECKING:
    from core.gamestate import GameState
    from entities.player import Player


class EmptyController(Controller):

    @property
    def name(self) -> str:
        return 'Empty'

    @property
    def is_ai(self) -> bool:
        return True

    def get_position(self, game_state: GameState, player: Player) -> Point:
        raise Exception('Empty can not make turn')


class PlayerController(Controller):
    @property
    def name(self) -> str:
        return 'Player'

    @property
    def is_ai(self) -> bool:
        return False

    def get_position(self, game_state: GameState, player: Player) -> Point:
        raise Exception('player not ai')


class RandomAI(Controller):
    @property
    def name(self) -> str:
        return 'Random AI'

    @property
    def is_ai(self) -> bool:
        return True

    def get_position(self, game_state: GameState, player: Player) -> Point:
        helper = game_state.game_helper
        available_pos = list(helper.get_available_positions(player))
        return random.choice(available_pos)


class SimpleAI(Controller):
    @property
    def name(self) -> str:
        return 'Simple AI'

    @property
    def is_ai(self) -> bool:
        return True

    def get_position(self, game_state: GameState, player: Player) -> Point:
        helper = game_state.game_helper
        available_pos = list(helper.get_available_positions(player))
        metric = self.ai_metric(player, game_state)
        positions = sorted(available_pos, key=metric, reverse=True)
        return positions[0]

    def ai_metric(self, current_player: Player,
                  game_state: GameState):
        return lambda point: self.metric(current_player, game_state, point)

    def metric(self, current_player: Player,
               game_state: GameState, point: Point) -> float:
        efficiency = self.metric_efficiency(current_player, game_state, point)
        security = self.metric_security(current_player, game_state, point)
        return efficiency * security

    def metric_efficiency(self, current_player: Player,
                          game_state: GameState, point: Point):
        helper = game_state.game_helper
        cell = game_state.game_field[point]
        if cell.real_owner == current_player:
            return 0
        enemy_count = 0
        for pos in game_state.get_near_position(point):
            if helper.is_enemy_point(pos, current_player):
                enemy_count += 1
        if enemy_count == 0:
            return 0
        else:
            return 1 / enemy_count

    def metric_security(self, current_player: Player,
                        game_state: GameState, point: Point):
        helper = game_state.game_helper
        if game_state.is_near_border(point):
            return 1
        near_count = 0
        near_sum = 0
        for pos in game_state.get_near_position(point):
            if helper.is_ally_point(pos, current_player):
                near_count += 1
                near_sum += 1
        for pos in helper.get_diagonal_points(point):
            if helper.is_ally_point(pos, current_player):
                near_count += 1
                near_sum += 0.5
        if near_count == 0:
            return 0
        else:
            return near_sum / near_count
