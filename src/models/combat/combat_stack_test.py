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

    actual = tuple(tuple(l) for l in stack.moves_remaining())
    expected = ((), (move_A,), (move_B,), (move_C, move_D))
    assert actual == expected
    assert stack.extract_resolved_moves() == ()


def test_advance_time_correct_stack():
    stack = CombatStack()

    stack.add_move(move_B, 2)
    stack.add_move(move_C, 3)
    stack.add_move(move_D, 3)
    stack.add_move(move_A, 1)

    stack.advance_time()
    actual = tuple(tuple(l) for l in stack.moves_remaining())
    expected = ((), (move_B,), (move_C, move_D))

    assert actual == expected
    assert stack.extract_resolved_moves() == (move_A,)

    stack.advance_time()
    actual = tuple(tuple(l) for l in stack.moves_remaining())
    expected = ((), (move_C, move_D))

    assert actual == expected
    assert stack.extract_resolved_moves() == (move_B,)

    stack.advance_time()
    actual = tuple(tuple(l) for l in stack.moves_remaining())
    expected = ((),)

    assert actual == expected
    assert stack.extract_resolved_moves() == (move_C, move_D)


def test_advance_time_called_before_extract_resolved():
    stack = CombatStack()

    stack.advance_time()  # No error after initialization.

    with pytest.raises(ValueError, match='extract_'):
        stack.advance_time()
