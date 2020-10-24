from __future__ import annotations
from graphic.colorscheme import ColorScheme
from graphic.scheme_parser import SchemeParser
from graphic.schemepreset import SchemePreset
from graphic.sizecontsants import SizeConstants
from graphic.graphicpaths import EMPTY_SCHEME_PATH


class Player:
    _empty_player = None

    def __init__(self, player_id: int, color_scheme: ColorScheme):
        self._id = player_id
        self._color_scheme = color_scheme
        self._score = 0

    @staticmethod
    def empty_player():
        if Player._empty_player is None:
            parser = SchemeParser(SizeConstants())
            empty_scheme = parser.get_scheme(EMPTY_SCHEME_PATH)
            Player._empty_player = Player(0, empty_scheme)
        return Player._empty_player

    @property
    def id(self):
        return self._id

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int):
        self._score = value

    @property
    def color_scheme(self) -> ColorScheme:
        return self._color_scheme
