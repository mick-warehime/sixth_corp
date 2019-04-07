from unittest import TestCase

from characters.character_examples import CharacterTypes
from characters.character_factory import build_character
from models.characters.subroutine_examples import DoNothing
from models.combat.ai_impl import AIType, build_ai


class ShuffleAITest(TestCase):

    def test_shuffle_ai_only_provides_usable_moves(self):
        user = build_character(CharacterTypes.HARMLESS.data)
        target = build_character(CharacterTypes.HARMLESS.data)
        ai = build_ai(AIType.Shuffle)
        ai.set_user(user)
        ai.set_targets([target])

        for _ in range(1000):
            move = ai.select_move()
            self.assertIsInstance(move.subroutine, DoNothing)

    def test_shuffle_ai_moves_dont_repeat(self):
        user = build_character(CharacterTypes.HARMLESS.data)
        target = build_character(CharacterTypes.HARMLESS.data)
        ai = build_ai(AIType.Shuffle)
        ai.set_user(user)
        ai.set_targets([target])

        prev_move_description = ''
        move_repeat_count = 0
        for _ in range(10000):
            move = ai.select_move()
            move_description = move.description()
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
        ai = build_ai(AIType.Shuffle)
        ai.set_user(user)
        ai.set_targets([target])

        with self.assertRaises(ValueError):
            ai.select_move()
