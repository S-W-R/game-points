from enum import Enum, auto


class ScoreRule(Enum):
    russian = auto()
    polish = auto()


class InitialPosition(Enum):
    empty = auto()
    cross = auto()
    double_cross = auto()
