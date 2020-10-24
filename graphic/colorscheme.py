from __future__ import annotations
from typing import Dict

from entities.celltype import CellType
from graphic.cellgraphic import CellGraphic


class ColorScheme:
    def __init__(self, name: str, scheme: Dict[CellType, CellGraphic]):
        self._name = name
        for i in CellType:
            if i not in scheme.keys():
                raise AttributeError()
        self._scheme = scheme

    @property
    def name(self):
        return self._name

    def __getitem__(self, item: CellType) -> CellGraphic:
        return self._scheme[item]
