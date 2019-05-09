import random

from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis import ChassisData
from models.characters.moves_base import Move
from models.characters.subroutines_base import build_subroutine
from models.combat.ai_impl import AIType, build_ai

# To ensure deterministic tests
random.seed(11)


def test_shuffle_ai_only_provides_usable_moves():
    usable = build_subroutine(can_use=True, num_cpu=0)
    unusable = build_subroutine(can_use=False)
    char_data = CharacterData(
        ChassisData(subroutines_granted=(usable, unusable)))
    user = build_character(data=char_data)
    target = build_character(data=char_data)
    ai = build_ai(AIType.Shuffle)
    ai.set_user(user)

    for _ in range(1000):
        move = ai.select_move([target])
        assert move.subroutine == usable


def test_shuffle_ai_moves_dont_repeat():
    do_nothing_0 = build_subroutine(description='0', num_cpu=0)
    do_nothing_1 = build_subroutine(description='1', num_cpu=0)
    unusable = build_subroutine(can_use=False, description='unusable')
    char_data = CharacterData(ChassisData(
        subroutines_granted=(do_nothing_0, do_nothing_1, unusable)))

    user = build_character(data=char_data)
    target = build_character(data=char_data)
    ai = build_ai(AIType.Shuffle)
    ai.set_user(user)

    prev_move_description = ''
    move_repeat_count = 0
    for _ in range(1000):
        move = ai.select_move([target])
        move_description = move.description()
        if move_description == prev_move_description:
            move_repeat_count += 1
        else:
            move_repeat_count = 0
        prev_move_description = move_description

        assert move_repeat_count <= 1


def test_no_valid_moves_means_do_nothing():
    no_subroutines = CharacterData(ChassisData())

    user = build_character(data=no_subroutines)
    target = build_character(data=no_subroutines)
    ai = build_ai(AIType.Shuffle)
    ai.set_user(user)

    # If no valid move exists, a null move is passed.
    move = ai.select_move([target])

    assert isinstance(move, Move)
