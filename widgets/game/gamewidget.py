from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPoint, QSize, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from const import rules
from entities.celltype import CellType
from geometry.point import Point

if TYPE_CHECKING:
    from core.gamestate import GameState


class GameWindow(QWidget):
    MIN_SIZE = QSize(400, 300)
    BACKGROUND_COLOR = QColor(220, 220, 220)

    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.__init_graphic()
        self.setMinimumSize(
            QSize(25 * game_state.width, 25 * game_state.height))
        # self.setGeometry(400, 400, 400, 400)

    def __init_graphic(self):
        self.graphic_label = QtWidgets.QLabel(self)
        # self.graphic_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.show()

    @staticmethod
    def min_size():
        return GameWindow.MIN_SIZE

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.draw_game_state()
        self.update()

    def mousePressEvent(self, mouse_event):
        if self.game_state.current_state != rules.CurrentState.player_playing:
            return
        pos = mouse_event.pos()
        self.game_state.player_make_turn(self.to_game_coordinates(pos))

    def mouseReleaseEvent(self, mouse_event):
        pass

    def minimumSizeHint(self):
        return self.min_size()

    def draw_game_state(self):
        size = self.size()
        canvas = QtGui.QPixmap(size)
        painter = QPainter(self.graphic_label)
        painter.begin(canvas)
        self.draw_background(painter)
        self.draw_game_field(painter)
        painter.end()
        self.graphic_label.adjustSize()
        self.graphic_label.setPixmap(canvas)

    def draw_background(self, painter: QPainter):
        rect = QRect(QPoint(0, 0), self.size())
        painter.setBrush(self.BACKGROUND_COLOR)
        painter.drawRect(rect)
        painter.setBrush(Qt.NoBrush)
        cell_width, cell_height = self.cell_size()
        for x in range(self.game_state.width):
            cell_start = self.to_widget_coordinates(Point(x, 0))
            line_x = cell_start + QPoint(int(cell_width) // 2, 0)
            painter.drawLine(line_x, line_x + QPoint(0, self.height()))
        for y in range(self.game_state.height):
            cell_start = self.to_widget_coordinates(Point(0, y))
            line_y = cell_start + QPoint(0, int(cell_height) // 2)
            painter.drawLine(line_y, line_y + QPoint(self.width(), 0))

    def draw_game_field(self, painter: QPainter):
        cell_width, cell_height = self.cell_size()
        game_field = self.game_state.game_field
        for x in range(self.game_state.width):
            for y in range(self.game_state.height):
                game_position = Point(x, y)
                cell = game_field[game_position]
                if cell.cell_type == CellType.empty:
                    continue
                cell_start = self.to_widget_coordinates(game_position)
                rect_center = cell_start + QPoint(int(cell_width) // 2,
                                                  int(cell_height) // 2)
                scheme = cell.graphic_owner.color_scheme[cell.cell_type]
                x_size = int(cell_width * scheme.size / 2)
                y_size = int(cell_height * scheme.size / 2)
                painter.setBrush(scheme.color)
                painter.drawEllipse(rect_center, x_size, y_size)
                painter.setBrush(Qt.NoBrush)

    def to_game_coordinates(self, pos: QPoint) -> Point:
        x = pos.x() // (self.width() // self.game_state.width)
        y = pos.y() // (self.height() // self.game_state.height)
        return Point(x, y)

    def to_widget_coordinates(self, point: Point):
        x = (self.width() // self.game_state.width) * point.x
        y = (self.height() // self.game_state.height) * point.y
        return QPoint(x, y)

    def cell_size(self) -> Tuple[float, float]:
        x = self.width() / self.game_state.width
        y = self.height() / self.game_state.height
        return x, y
