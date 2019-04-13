"""Tests for CombatStack."""
from unittest.mock import Mock

import pytest

from models.combat.combat_stack import CombatStack
from models.combat.moves_base import Move

move_A = Mock(Move, name='A')
move_B = Mock(Move, name='B')
move_C = Mock(Move, name='C')
move_D = Mock(Move, name='D')


def test_extract_resolved_after_init():
    stack = CombatStack()

    assert stack.extract_resolved_moves() == ()


def test_moves_remaining_correct_order():
    stack = CombatStack()

    stack.add_move(move_B, 2)
    stack.add_move(move_C, 3)
    stack.add_move(move_D, 3)
    stack.add_move(move_A, 1)

    actual = tuple(stack.moves_times_remaining())
    expected = ((move_A, 1), (move_B, 2), (move_C, 3), (move_D, 3))
    assert actual == expected
    assert stack.extract_resolved_moves() == ()


def test_advance_time_correct_stack():
    stack = CombatStack()

    stack.add_move(move_B, 2)
    stack.add_move(move_C, 3)
    stack.add_move(move_D, 3)
    stack.add_move(move_A, 1)

    stack.advance_time()
    actual = tuple(stack.moves_times_remaining())
    expected = ((move_B, 1), (move_C, 2), (move_D, 2))

    assert actual == expected
    assert stack.extract_resolved_moves() == (move_A,)

    stack.advance_time()
    actual = tuple(stack.moves_times_remaining())
    expected = ((move_C, 1), (move_D, 1))

    assert actual == expected
    assert stack.extract_resolved_moves() == (move_B,)

    stack.advance_time()
    actual = tuple(stack.moves_times_remaining())
    expected = ()

    assert actual == expected
    assert stack.extract_resolved_moves() == (move_C, move_D)


def test_advance_time_called_before_extract_resolved():
    stack = CombatStack()

    stack.advance_time()  # No error after initialization.

    with pytest.raises(ValueError, match='extract_'):
        stack.advance_time()
