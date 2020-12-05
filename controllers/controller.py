from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geometry.point import Point
    from core.gamestate import GameState
    from entities.player import Player


class Controller(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_ai(self) -> bool:
        pass

    @abstractmethod
    def get_position(self, game_state: GameState, player: Player) -> Point:
        pass
