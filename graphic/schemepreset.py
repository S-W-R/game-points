from __future__ import annotations

from typing import Iterable

from graphic.colorscheme import ColorScheme
from graphic.graphicpaths import MAIN_SCHEME_PATH
from graphic.scheme_parser import SchemeParser
from graphic.sizecontsants import SizeConstants


class SchemePreset:
    def __init__(self, size_constants: SizeConstants = SizeConstants()):
        parser = SchemeParser(size_constants)
        self._schemes = dict()
        for i in parser.get_schemes(MAIN_SCHEME_PATH):
            self._schemes[i.name] = i

    def __len__(self):
        return len(self._schemes)

    def __getitem__(self, item: str) -> ColorScheme:
        return self._schemes[item]

    def __iter__(self) -> Iterable[ColorScheme]:
        for i in self._schemes.values():
            yield i
