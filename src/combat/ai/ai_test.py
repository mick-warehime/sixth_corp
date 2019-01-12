from unittest import TestCase

from parameterized import parameterized

from characters.enemies.useless import UselessBuilder
from combat.ai.ai_factory import AIType, build_ai

AI_TYPES = [[AIType.Random], [AIType.Shuffle]]


class AITest(TestCase):
    """Tests that every AI should conform to."""

    @parameterized.expand(AI_TYPES)
    def test_no_valid_moves_raises(self, ai_type):
        user = UselessBuilder().build()
        ai = build_ai(user, ai_type)
        target = UselessBuilder().build()
        ai.set_targets([target])

        with self.assertRaises(AssertionError):
            ai.select_move()