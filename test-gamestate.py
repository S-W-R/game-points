import unittest

from const.controllers import ControllerType
from const.rules import InitialPosition, ScoreRule, CurrentState
from controllers.controller import Controller
from core.gamestate import GameState
from entities.cell import Cell
from entities.player import Player
from geometry.matrix import Matrix
from geometry.point import Point


class GameStateTestCase(unittest.TestCase):
    SURROUNDED_TEST_FIELD = [
        {Point(1, 1), Point(1, 2), Point(2, 2), Point(5, 0), Point(4, 1),
         Point(6, 1), Point(5, 2)},
        {Point(1, 0), Point(2, 0), Point(1, 3), Point(2, 3), Point(0, 1),
         Point(0, 2), Point(3, 1), Point(3, 2)}]

    def test_surrounding(self):
        game_state = self.__create_default_game_state(ScoreRule.russian)
        first_player_pos = self.SURROUNDED_TEST_FIELD[0]
        second_player_pos = self.SURROUNDED_TEST_FIELD[1]
        surrounded = (Point(x, y) for x in range(1, 3) for y in range(1, 3))
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        for pos in first_player_pos:
            game_state.make_turn(pos, first_player)
        for pos in second_player_pos:
            game_state.make_turn(pos, second_player)
        for pos in self._iterate_over_game_field(game_state.game_field):
            cell = game_state.game_field[pos]
            if (cell.position in surrounded
                    and cell.real_owner != second_player):
                self.fail()

    def test_russian_score_rules_on_surrounded_test(self):
        game_state = self.__init_surrounded_test_game_state(ScoreRule.russian)
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        self.assertEqual(first_player.score, 0)
        self.assertEqual(second_player.score, 3)

    def test_polish_score_rules_on_surrounded_test(self):
        game_state = self.__init_surrounded_test_game_state(ScoreRule.polish)
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        self.assertEqual(first_player.score, 1)
        self.assertEqual(second_player.score, 7)

    def test_russian_score_rule_on_empty_surrounded(self):
        game_state = self.__init_empty_surrounded_test_game_state(
            ScoreRule.russian)
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        self.assertEqual(first_player.score, 0)
        self.assertEqual(second_player.score, 0)

    def test_polish_score_rule_on_empty_surrounded(self):
        game_state = self.__init_empty_surrounded_test_game_state(
            ScoreRule.polish)
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        self.assertEqual(first_player.score, 1)
        self.assertEqual(second_player.score, 0)

    def __init_empty_surrounded_test_game_state(self, score_rule: ScoreRule):
        game_state = self.__create_default_game_state(score_rule)
        first_player_pos = {Point(1, 0), Point(0, 1), Point(2, 1), Point(1, 2)}
        first_player = game_state.players[0]
        for pos in first_player_pos:
            game_state.make_turn(pos, first_player)
        return game_state

    def __init_surrounded_test_game_state(self, score_rule: ScoreRule):
        game_state = self.__create_default_game_state(score_rule)
        first_player_pos = self.SURROUNDED_TEST_FIELD[0]
        second_player_pos = self.SURROUNDED_TEST_FIELD[1]
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        for pos in first_player_pos:
            game_state.make_turn(pos, first_player)
        for pos in second_player_pos:
            game_state.make_turn(pos, second_player)
        return game_state

    def test_not_surrounding(self):
        game_state = self.__create_default_game_state(ScoreRule.russian)
        first_player_pos = {Point(0, 0), Point(2, 0), Point(1, 1)}
        second_player_pos = {Point(1, 0), Point(3, 0), Point(0, 1),
                             Point(2, 1)}
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        for pos in first_player_pos:
            game_state.make_turn(pos, first_player)
        for pos in second_player_pos:
            game_state.make_turn(pos, second_player)
        for pos in first_player_pos:
            if game_state.game_field[pos].real_owner != first_player:
                self.fail()

    def test_correct_turn(self):
        game_state = self.__create_default_game_state(ScoreRule.russian)
        first_player_pos = {Point(1, 1), Point(2, 1), Point(5, 2)}
        second_player_pos = {Point(1, 0), Point(2, 0), Point(1, 3),
                             Point(2, 3), Point(0, 1), Point(0, 2),
                             Point(3, 1), Point(3, 2)}
        not_empty_pos = first_player_pos | second_player_pos
        empty_surrounded_positions = {Point(1, 2), Point(2, 2)}

        first_player = game_state.players[0]
        second_player = game_state.players[1]
        for pos in first_player_pos:
            game_state.make_turn(pos, first_player)
        for pos in second_player_pos:
            game_state.make_turn(pos, second_player)
        for pos in self._iterate_over_game_field(game_state.game_field):
            if pos in not_empty_pos:
                self.assertFalse(game_state.is_correct_turn(pos, first_player))
                self.assertFalse(
                    game_state.is_correct_turn(pos, second_player))
            elif pos in empty_surrounded_positions:
                self.assertFalse(game_state.is_correct_turn(pos, first_player))
                self.assertTrue(game_state.is_correct_turn(pos, second_player))
            else:
                self.assertTrue(game_state.is_correct_turn(pos, first_player))
                self.assertTrue(game_state.is_correct_turn(pos, second_player))

    def test_player_make_turn(self):
        game_state = self.__create_default_game_state(ScoreRule.russian)
        first_player_pos = Point(0, 0)
        second_player_pos = Point(1, 0)
        first_player = game_state.players[0]
        second_player = game_state.players[1]
        game_state.player_make_turn(first_player_pos)
        game_state.player_make_turn(second_player_pos)
        for pos in self._iterate_over_game_field(game_state.game_field):
            cell = game_state.game_field[pos]
            if pos == first_player_pos:
                if cell.real_owner != first_player:
                    self.fail()
            elif pos == second_player_pos:
                if cell.real_owner != second_player:
                    self.fail()
            elif cell.real_owner != game_state.empty_player:
                self.fail()

    def test_ai_make_turn(self):
        class TargetAi(Controller):
            def __init__(self, position_to_move: Point):
                super().__init__()
                self._position_to_move = position_to_move

            @property
            def name(self) -> str:
                return ''

            @property
            def is_ai(self) -> bool:
                return True

            def get_position(self, game_state: GameState,
                             player: Player) -> Point:
                return self._position_to_move

        first_player_pos = Point(0, 0)
        second_player_pos = Point(1, 0)
        first_player = Player(1, None, TargetAi(first_player_pos))
        second_player = Player(2, None, TargetAi(second_player_pos))
        game_state = GameState(size=Point(10, 10),
                               score_rule=ScoreRule.russian,
                               initial_position=InitialPosition.empty,
                               players=(first_player, second_player))
        game_state.ai_make_turn()
        game_state.ai_make_turn()
        for pos in self._iterate_over_game_field(game_state.game_field):
            cell = game_state.game_field[pos]
            if pos == first_player_pos:
                if cell.real_owner != first_player:
                    self.fail()
            elif pos == second_player_pos:
                if cell.real_owner != second_player:
                    self.fail()
            elif cell.real_owner != game_state.empty_player:
                self.fail()

    def test_game_ended(self):
        game_state = self.__create_default_game_state(
            score_rule=ScoreRule.russian)
        for pos in self._iterate_over_game_field(game_state.game_field):
            game_state.player_make_turn(pos)
        if game_state.current_state != CurrentState.ended:
            self.fail()

    def _iterate_over_game_field(self, game_field: Matrix[Cell]):
        for x in range(game_field.width):
            for y in range(game_field.height):
                yield Point(x, y)

    def __create_default_game_state(self, score_rule: ScoreRule) -> GameState:
        empty_scheme = None
        player1 = Player(1, empty_scheme, ControllerType.player.value)
        player2 = Player(2, empty_scheme, ControllerType.player.value)
        return GameState(size=Point(10, 10),
                         initial_position=InitialPosition.empty,
                         score_rule=score_rule,
                         players=(player1, player2))


if __name__ == '__main__':
    unittest.main()
