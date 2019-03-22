from unittest import TestCase

from characters.character_examples import CharacterTypes
from characters.character_factory import build_character
from characters.subroutine_examples import Harmless
from combat.shuffle_ai import ShuffleAI


class ShuffleAITest(TestCase):

    def test_shuffle_ai_only_provides_usable_moves(self):
        user = build_character(CharacterTypes.HARMLESS.data)
        target = build_character(CharacterTypes.HARMLESS.data)
        ai = ShuffleAI()
        ai.set_user(user)
        ai.set_targets([target])

        for i in range(1000):
            move = ai.select_move()
            self.assertIsInstance(move.subroutine, Harmless)

    def test_shuffle_ai_moves_dont_repeat(self):
        user = build_character(CharacterTypes.HARMLESS.data)
        target = build_character(CharacterTypes.HARMLESS.data)
        ai = ShuffleAI()
        ai.set_user(user)
        ai.set_targets([target])

        prev_move_description = ''
        move_repeat_count = 0
        for i in range(10000):
            move = ai.select_move()
            move_description = move.describe()
            if move_description == prev_move_description:
                move_repeat_count += 1
            else:
                move_repeat_count = 0
            prev_move_description = move_description

            # the most a move can repeat is 2 times - assuming unique moves
            # and all moves get played before reshuffle
            # [1,2] -> [2, 1] -> [1, 2]
            self.assertLess(move_repeat_count, 3)

    def test_no_valid_moves_raises(self):
        user = build_character(CharacterTypes.USELESS.data)
        target = build_character(CharacterTypes.USELESS.data)
        ai = ShuffleAI()
        ai.set_user(user)
        ai.set_targets([target])

        with self.assertRaises(AssertionError):
            ai.select_move()
