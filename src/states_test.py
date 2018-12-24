"""Tests for states.py"""

from states import Stateful, Attribute, IsDead, State, HasState


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


def test_condition_and():
    stateful = Stateful()

    cond = HasState(State.ON_FIRE) & IsDead()
    assert not cond.check(stateful)
    stateful.set_state(State.ON_FIRE, True)
    assert cond.check(stateful)

    assert not (cond & HasState(State.INANIMATE)).check(stateful)
