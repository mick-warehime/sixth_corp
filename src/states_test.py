"""Tests for states.py"""

from states import HasState, Attribute, IsDead, State


def test_alive_to_dead():
    stateful = HasState()

    assert IsDead.check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 3)
    assert not IsDead.check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 0)
    assert IsDead.check(stateful)

def test_str_methods():
    assert str(State.ON_FIRE)=='on fire'
    assert str(Attribute.HEALTH)=='health'