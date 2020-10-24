from enum import Enum, auto


class Rule:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class ScoreRule(Enum):
    russian = Rule('russian')
    polish = Rule('polish')


class InitialPosition(Enum):
    empty = Rule('empty')
    cross = Rule('cross')
    double_cross = Rule('double cross')


RULE_FROM_NAME = {
    'russian': ScoreRule.russian,
    'polish': ScoreRule.polish,
    'empty': InitialPosition.empty,
    'cross': InitialPosition.cross,
    'double cross': InitialPosition.double_cross
}
