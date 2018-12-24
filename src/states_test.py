"""Tests for states.py"""

from states import Stateful, Attribute, State
from conditions import IsDead


def test_alive_to_dead():
    stateful = Stateful()

    assert IsDead.check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 3)
    assert not IsDead.check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 0)
    assert IsDead.check(stateful)


def test_str_methods():
    assert str(State.ON_FIRE) == 'on fire'
    assert str(Attribute.HEALTH) == 'health'


