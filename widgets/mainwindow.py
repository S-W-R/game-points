from __future__ import annotations

import pickle
from collections import deque
from typing import TYPE_CHECKING

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from const import rules
from const.actions import ActionType
from const.rules import CurrentState
from widgets.game.gamewidget import GameWindow
from widgets.game.menuwidget import MenuWidget

if TYPE_CHECKING:
    from core.gamestate import GameState


class MainWindow(QWidget):
    MAX_STACK_SIZE = 5

    def __init__(self, game_state: GameState):
        super().__init__()
        self.game_state = game_state
        self.__init_game_states_stack()
        self.__init_window(game_state)

    def __init_window(self, game_state: GameState):
        layout = QHBoxLayout(self)
        self.game_widget = GameWindow(game_state, self)
        self.menu_widget = MenuWidget(game_state, self)
        layout.addWidget(self.game_widget)
        layout.addWidget(self.menu_widget)
        layout.setStretch(0, 10)
        layout.setStretch(1, 0)
        self.setLayout(layout)
        self.setWindowTitle("Points")
        # self.setMinimumSize(GameWindow.min_size())
        self.__init_timer()
        self.show()

    def __init_game_states_stack(self):
        self._undo_stack = deque(maxlen=self.MAX_STACK_SIZE)
        self._redo_stack = deque(maxlen=self.MAX_STACK_SIZE)
        self.update_game_state_with_action(ActionType.game_initialized)

    def __init_timer(self):
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.__update_game_state)
        self.game_timer.start(100)

    def __update_game_state(self):
        if self.game_state.current_state == rules.CurrentState.ai_playing:
            self.update_game_state_with_action(ActionType.ai_make_turn)
            self.game_state.ai_make_turn()
            self.notify_game_state_changed()
        elif self.game_state.current_state == rules.CurrentState.ended:
            self.setWindowTitle('Points: game over')
            self.game_timer.stop()

    def __set_new_game_state(self, new_game_state: GameState):
        self.game_state.copy_fields_from_another_game_state(new_game_state)
        self.update()

    def notify_game_state_changed(self):
        self.update()

    def update_game_state_with_action(self, action_type: ActionType):
        if self.game_state.current_state == CurrentState.ended:
            return
        if action_type in (ActionType.game_initialized,
                           ActionType.ai_make_turn):
            pass
        elif action_type == ActionType.player_make_turn:
            if self.game_state.current_state == CurrentState.player_playing:
                self._undo_stack.append(pickle.dumps(self.game_state))
                self._redo_stack.clear()
        elif action_type == ActionType.player_undo_turn:
            if len(self._undo_stack) > 0:
                self._redo_stack.append(pickle.dumps(self.game_state))
                new_game_state = pickle.loads(self._undo_stack.pop())
                self.__set_new_game_state(new_game_state)
        elif action_type == ActionType.player_redo_turn:
            if len(self._redo_stack) > 0:
                self._undo_stack.append(pickle.dumps(self.game_state))
                new_game_state = pickle.loads(self._redo_stack.pop())
                self.__set_new_game_state(new_game_state)
        else:
            raise AttributeError(f'unknown action type: {ActionType}')

    def undo_turn(self):
        self.update_game_state_with_action(ActionType.player_undo_turn)

    def redo_turn(self):
        self.update_game_state_with_action(ActionType.player_redo_turn)
