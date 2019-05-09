"""Tests for CombatStack."""
from unittest.mock import Mock

import pytest

from models.characters.moves_base import Move
from models.characters.subroutines_base import build_subroutine
from models.combat.combat_stack import CombatStack

time_1_sub = build_subroutine(time_to_resolve=1)
time_2_sub = build_subroutine(time_to_resolve=2)
time_3_sub = build_subroutine(time_to_resolve=3)

move_1 = Mock(Move, name='1 turns', subroutine=time_1_sub)
move_2 = Mock(Move, name='2 turns', subroutine=time_2_sub)
move_3_A = Mock(Move, name='3 turns A', subroutine=time_3_sub)
move_3_B = Mock(Move, name='3 turns B', subroutine=time_3_sub)


def test_resolved_moves_after_init():
    stack = CombatStack()

    assert stack.resolved_moves() == ()


def test_moves_remaining_correct_order():
    stack = CombatStack()

    for m in [move_2, move_3_A, move_3_B, move_1]:
        stack.add_move(m, m.subroutine.time_to_resolve())

    actual = tuple(stack.moves_times_remaining())
    expected = ((move_1, 1), (move_2, 2), (move_3_A, 3), (move_3_B, 3))
    assert actual == expected
    assert stack.resolved_moves() == ()


def test_update_multiple_times_correct_stack():
    stack = CombatStack()

    for m in [move_2, move_3_A, move_3_B, move_1]:
        stack.add_move(m, m.subroutine.time_to_resolve())
    assert stack.resolved_moves() == ()

    stack.advance_time()
    actual = tuple(stack.moves_times_remaining())
    expected = ((move_2, 1), (move_3_A, 2), (move_3_B, 2))

    assert actual == expected
    assert stack.resolved_moves() == (move_1,)

    stack.advance_time()
    actual = tuple(stack.moves_times_remaining())
    expected = ((move_3_A, 1), (move_3_B, 1))

    assert actual == expected
    assert stack.resolved_moves() == (move_2,)

    stack.advance_time()
    actual = tuple(stack.moves_times_remaining())
    expected = ()

    assert actual == expected
    assert stack.resolved_moves() == (move_3_A, move_3_B)


def test_update_stack_called_before_execute_resolved():
    stack = CombatStack()

    stack.advance_time()  # No error after initialization.

    with pytest.raises(ValueError, match='execute_resolved'):
        stack.advance_time()
