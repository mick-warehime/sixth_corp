import random
from unittest import TestCase

from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis_examples import ChassisData
from models.characters.subroutines_base import build_subroutine
from models.combat.ai_impl import AIType, build_ai

# To ensure deterministic tests
random.seed(11)


def test_shuffle_ai_only_provides_usable_moves():
    usable = build_subroutine(can_use=True)
    unusable = build_subroutine(can_use=False)
    char_data = CharacterData(
        ChassisData(subroutines_granted=(usable, unusable)))
    user = build_character(char_data)
    target = build_character(char_data)
    ai = build_ai(AIType.Shuffle)
    ai.set_user(user)
    ai.set_targets([target])

    for _ in range(1000):
        move = ai.select_move()
        assert move.subroutine == usable


def test_shuffle_ai_moves_dont_repeat():
    do_nothing_0 = build_subroutine(description='0')
    do_nothing_1 = build_subroutine(description='1')
    unusable = build_subroutine(can_use=False, description='unusable')
    char_data = CharacterData(ChassisData(
        subroutines_granted=(do_nothing_0, do_nothing_1, unusable)))

    user = build_character(char_data)
    target = build_character(char_data)
    ai = build_ai(AIType.Shuffle)
    ai.set_user(user)
    ai.set_targets([target])

    prev_move_description = ''
    move_repeat_count = 0
    for _ in range(1000):
        move = ai.select_move()
        move_description = move.description()
        if move_description == prev_move_description:
            move_repeat_count += 1
        else:
            move_repeat_count = 0
        prev_move_description = move_description

        assert move_repeat_count <= 1


def test_no_valid_moves_means_do_nothing():
    no_subroutines = CharacterData(ChassisData())

    user = build_character(no_subroutines)
    target = build_character(no_subroutines)
    ai = build_ai(AIType.Shuffle)
    ai.set_user(user)
    ai.set_targets([target])

    move = ai.select_move()

    print(move)
