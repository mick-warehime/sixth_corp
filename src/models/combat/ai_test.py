from unittest import TestCase

from parameterized import parameterized

from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis import ChassisData
from models.characters.subroutines_base import build_subroutine
from models.combat.ai_impl import AIType, build_ai

AI_TYPES = [[AIType.Random], [AIType.Shuffle]]


class AITest(TestCase):
    """Tests that every AI should conform to."""

    @parameterized.expand(AI_TYPES)
    def test_no_valid_moves_gives_default_move(self, ai_type):
        unusable = build_subroutine(can_use=False)
        data = CharacterData(ChassisData(subroutines_granted=(unusable,)))
        user = build_character(data=data)
        ai = build_ai(ai_type)
        ai.set_user(user)
        target = build_character(data=data)

        move_comps = set()
        for _ in range(100):
            move = ai.select_move([target])
            sub = move.subroutine
            components = (
                sub.cpu_slots(), sub.time_to_resolve(), sub.description())
            move_comps.add(components)

        assert len(move_comps) == 1
