import json
from typing import Iterable, List

from PyQt5.QtGui import QColor

from entities.celltype import CellType
from graphic.cellgraphic import CellGraphic
from graphic.colorscheme import ColorScheme
from graphic.sizecontsants import SizeConstants


class SchemeParser:
    def __init__(self, size_constants: SizeConstants):
        self._size_constants = size_constants

    def get_scheme(self, filename: str) -> ColorScheme:
        with open(filename, mode='r', encoding='utf8') as json_data:
            data = json.load(json_data)
            name = data['name']
            raw_scheme = data['scheme']
            return self.__parse_color_scheme(name, raw_scheme)

    def get_schemes(self, filename: str) -> Iterable[ColorScheme]:
        with open(filename, mode='r', encoding='utf8') as json_data:
            data = json.load(json_data)
        for i in data:
            name = i['name']
            raw_scheme = i['scheme']
            yield self.__parse_color_scheme(name, raw_scheme)

    def __parse_color_scheme(self, name: str, raw_scheme) -> ColorScheme:
        scheme = dict()
        scheme[CellType.empty] = self.__parse_cell_graphic(
            raw_scheme['empty'])
        scheme[CellType.captured_cell] = self.__parse_cell_graphic(
            raw_scheme['captured'])
        scheme[CellType.active_point] = self.__parse_cell_graphic(
            raw_scheme['active'])
        scheme[CellType.inactive_point] = self.__parse_cell_graphic(
            raw_scheme['inactive'])
        return ColorScheme(name, scheme)

    def __parse_cell_graphic(self, raw_cell_scheme) -> CellGraphic:
        return CellGraphic(
            self.__parse_size(raw_cell_scheme['size']),
            self.__parse_color(raw_cell_scheme['color']))

    def __parse_color(self, color_information: List[int]) -> QColor:
        if len(color_information) != 4:
            raise AttributeError()
        red = color_information[0]
        green = color_information[1]
        blue = color_information[2]
        alpha = color_information[3]
        return QColor(red, green, blue, alpha)

    def __parse_size(self, raw_size) -> float:
        return (self._size_constants[raw_size['size']]
                if raw_size['is_constant']
                else raw_size['size'])
