from unittest import TestCase

from parameterized import parameterized

from characters.character_examples import CharacterData
from characters.character_impl import build_character
from models.characters.chassis_examples import ChassisData
from models.characters.subroutine_examples import Unusable
from models.combat.ai_impl import AIType, build_ai

AI_TYPES = [[AIType.Random], [AIType.Shuffle]]


class AITest(TestCase):
    """Tests that every AI should conform to."""

    @parameterized.expand(AI_TYPES)
    def test_no_valid_moves_raises(self, ai_type):
        data = CharacterData(ChassisData(subroutines_granted=(Unusable(1),)))
        user = build_character(data)
        ai = build_ai(ai_type)
        ai.set_user(user)
        target = build_character(data)
        ai.set_targets([target])

        with self.assertRaises(ValueError):
            ai.select_move()

    def test_human_ai_raises_error(self):
        data = CharacterData(ChassisData(subroutines_granted=(Unusable(1),)))
        user = build_character(data)
        ai = build_ai(AIType.Human)
        ai.set_user(user)
        target = build_character(data)
        ai.set_targets([target])

        with self.assertRaises(NotImplementedError):
            ai.select_move()
