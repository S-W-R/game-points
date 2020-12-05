from enum import Enum, auto


class Rule:
    def __init__(self, name):
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class ScoreRule(Enum):
    russian = Rule('russian')
    polish = Rule('polish')


class InitialPosition(Enum):
    empty = Rule('empty')
    cross = Rule('cross')
    double_cross = Rule('double cross')


class CurrentState(Enum):
    player_playing = auto()
    ai_playing = auto()
    ended = auto()


SCORE_RULE_FROM_NAME = {i.value.name: i for i in ScoreRule}
INITIAL_POSITION_FROM_RULE = {i.value.name: i for i in InitialPosition}
