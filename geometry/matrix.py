from __future__ import annotations
from typing import List, NoReturn, TypeVar, Generic

from geometry.point import Point

T = TypeVar('T')


class Matrix(Generic[T]):
    value: T

    def __init__(self, width: int, height: int):
        if width < 0 or height < 0:
            raise ValueError()
        self._width = width
        self._height = height
        self._matrix = self.__init_matrix(self._width, self._height)

    @staticmethod
    def __init_matrix(width: int, height: int) -> List[List[T]]:
        matrix = list()
        for i in range(width):
            column = list()
            matrix.append(column)
            for j in range(height):
                column.append(None)
        return matrix

    @staticmethod
    def from_point(point: Point) -> Matrix:
        return Matrix(point.x, point.y)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def in_borders(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def __getitem__(self, key: Point) -> T:
        if not self.in_borders(key.x, key.y):
            raise IndexError()
        return self._matrix[key.x][key.y]

    def __setitem__(self, key: Point, value: T) -> NoReturn:
        if not self.in_borders(key.x, key.y):
            raise IndexError()
        self._matrix[key.x][key.y] = value
