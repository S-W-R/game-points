from enum import Enum, auto


class ActionType(Enum):
    game_initialized = auto()
    player_make_turn = auto()
    ai_make_turn = auto()
    player_undo_turn = auto()
    player_redo_turn = auto()
