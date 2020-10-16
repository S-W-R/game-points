from typing import Dict

from entities.cell import CellTypes
from graphic.cellgraphic import CellGraphic


class ColorScheme:
    def __init__(self, scheme: Dict[CellTypes, CellGraphic]):
        for i in CellTypes:
            if i not in scheme.keys():
                raise AttributeError()
        self._scheme = scheme

    def __getitem__(self, item: CellTypes) -> CellGraphic:
        return self._scheme[item]


