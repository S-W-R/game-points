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
        return Point(0,0)

    def ai_metric(self, current_player: Player,
                  game_state: GameState, point: Point) -> float:
        return 0
