from __future__ import annotations


class Point:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @staticmethod
    def zero() -> Point:
        return Point(0, 0)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, obj):
        return isinstance(obj, Point) and obj.x == self.x and obj.y == self.y

    def __ne__(self, obj):
        return not self == obj

    def __hash__(self):
        return 397 * self.x.__hash__() ** self.y.__hash__()

    def __str__(self):
        return f"x: {self.x}; y: {self.y};"
