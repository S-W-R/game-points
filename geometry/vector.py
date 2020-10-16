from __future__ import annotations
import math


class Vector:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        self._length = math.sqrt(self._x * self._x + self._y * self._y)

    @property
    def length(self) -> float:
        return self._length

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def angle(self) -> float:
        return math.atan2(self._y, self._x)

    def rotate(self, angle: float) -> Vector:
        return Vector(self.x * math.cos(angle) - self.y * math.sin(angle),
                      self.x * math.sin(angle) + self.y * math.cos(angle))

    def multiple(self, k: float) -> Vector:
        return Vector(self.x * k, self.y * k)

    def div(self, k: float) -> Vector:
        return Vector(self.x / k, self.y / k)

    def normalize(self) -> Vector:
        return self.div(self.length) if self.length > 0 else self

    def normalize_to(self, new_length: float):
        return self.multiple(new_length / self.length) \
            if self.length > 0 else self

    def angle_between(self, other_vector: Vector) -> float:
        return math.acos((self.x * other_vector.x + self.y * other_vector.y) /
                         (self.length * other_vector.length))

    @staticmethod
    def zero():
        return Vector(0, 0)

    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, obj):
        return isinstance(obj, Vector) and obj.x == self.x and obj.y == self.y

    def __ne__(self, obj):
        return not self == obj

    def __hash__(self):
        return 397 * self.x.__hash__() ** self.y.__hash__()

    def __str__(self):
        return f"x: {self.x}; y: {self.y};"
