from graphic.colorscheme import ColorScheme
from graphic.schemepreset import SchemePreset


class Player:
    _empty_player = None

    def __init__(self, player_id: int, color_scheme: ColorScheme):
        self._id = player_id
        self._color_scheme = color_scheme
        self._score = 0

    @staticmethod
    def empty_player():
        if Player._empty_player is None:
            Player._empty_player = Player(0, SchemePreset.empty.value)
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
