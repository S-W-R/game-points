from __future__ import annotations
from typing import Iterable, Tuple, List
import json
from PyQt5.QtGui import QColor

from entities.celltype import CellType
from graphic.cellgraphic import CellGraphic
from graphic.colorscheme import ColorScheme
from graphic.scheme_parser import SchemeParser
from graphic.sizecontsants import SizeConstants
from graphic.graphicpaths import MAIN_SCHEME_PATH


class SchemePreset:
    def __init__(self, size_constants: SizeConstants = SizeConstants()):
        parser = SchemeParser(size_constants)
        self._schemes = dict()
        for i in parser.get_schemes(MAIN_SCHEME_PATH):
            self._schemes[i.name] = i

    def __getitem__(self, item: str) -> ColorScheme:
        return self._schemes[item]

    def __iter__(self) -> Iterable[ColorScheme]:
        return self._schemes.values()
