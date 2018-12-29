"""Tests for states.py"""

from models.states import Attribute, State


def test_str_methods():
    assert str(State.ON_FIRE) == 'on fire'
    assert str(Attribute.HEALTH) == 'health'