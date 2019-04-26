"""Tests for CombatStack."""
from unittest.mock import Mock

import pytest

from models.characters.subroutines_base import build_subroutine
from models.combat.combat_stack import CombatStack
from models.characters.moves_base import Move

time_1_sub = build_subroutine(time_to_resolve=1)
time_2_sub = build_subroutine(time_to_resolve=2)
time_3_sub = build_subroutine(time_to_resolve=3)

move_1 = Mock(Move, name='1 turns', subroutine=time_1_sub)
move_2 = Mock(Move, name='2 turns', subroutine=time_2_sub)
move_3_A = Mock(Move, name='3 turns A', subroutine=time_3_sub)
move_3_B = Mock(Move, name='3 turns B', subroutine=time_3_sub)


def test_resolved_moves_after_init():
    stack = CombatStack()

    assert stack.resolved_moves == ()


def test_moves_remaining_correct_order():
    stack = CombatStack()

    stack.update_stack([move_2, move_3_A, move_3_B, move_1])

    actual = tuple(stack.moves_times_remaining())
    expected = ((move_1, 1), (move_2, 2), (move_3_A, 3), (move_3_B, 3))
    assert actual == expected
    assert stack.resolved_moves == ()


def test_update_multiple_times_correct_stack():
    stack = CombatStack()

    stack.update_stack([move_2, move_3_A, move_3_B, move_1])
    stack.execute_resolved_moves()  # must be called once before each update

    stack.update_stack([])
    actual = tuple(stack.moves_times_remaining())
    expected = ((move_2, 1), (move_3_A, 2), (move_3_B, 2))
    stack.execute_resolved_moves()

    assert actual == expected
    assert stack.resolved_moves == (move_1,)

    stack.update_stack([])
    stack.execute_resolved_moves()
    actual = tuple(stack.moves_times_remaining())
    expected = ((move_3_A, 1), (move_3_B, 1))

    assert actual == expected
    assert stack.resolved_moves == (move_2,)

    stack.update_stack([])
    actual = tuple(stack.moves_times_remaining())
    expected = ()
    stack.execute_resolved_moves()

    assert actual == expected
    assert stack.resolved_moves == (move_3_A, move_3_B)


def test_update_stack_called_before_execute_resolved():
    stack = CombatStack()

    stack.update_stack([])  # No error after initialization.

    with pytest.raises(ValueError, match='execute_resolved'):
        stack.update_stack([])


def test_execute_resolved_called_twice():
    stack = CombatStack()

    stack.update_stack([])  # No error after initialization.
    stack.execute_resolved_moves()

    with pytest.raises(ValueError, match='update_stack'):
        stack.execute_resolved_moves()


def test_prestack_method_called_on_each_move():
    moves_invoked = []

    def prestack_fun(move):
        moves_invoked.append(move)

    stack = CombatStack(prestack_fun)

    expected = (move_1, move_2, move_3_A, move_3_B)
    stack.update_stack(expected)

    actual = tuple(moves_invoked)
    assert actual == expected


def test_poststack_method_called_on_each_move():
    moves_invoked = []

    def poststack_fun(move):
        moves_invoked.append(move)

    stack = CombatStack(poststack_fun=poststack_fun)

    stack.update_stack((move_1, move_2, move_3_A, move_3_B))

    assert not moves_invoked

    stack.execute_resolved_moves()  # no moves have resolved yet
    actual = tuple(moves_invoked)
    expected = ()
    assert actual == expected

    for _ in range(4):
        stack.update_stack([])
        stack.execute_resolved_moves()
        actual = tuple(moves_invoked)
        expected = expected + tuple(stack.resolved_moves)
        assert actual == expected
