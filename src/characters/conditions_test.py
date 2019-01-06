from characters.conditions import HasState, IsDead
from characters.states import BasicStatus, State, Attribute


def test_condition_and():
    stateful = BasicStatus()

    cond = HasState(State.ON_FIRE) & IsDead()
    assert not cond.check(stateful)
    stateful.set_state(State.ON_FIRE, True)
    assert cond.check(stateful)

    assert not (cond & HasState(State.FROZEN)).check(stateful)


def test_condition_or():
    stateful = BasicStatus()

    cond = HasState(State.ON_FIRE) | IsDead()
    assert cond.check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 1)
    assert not cond.check(stateful)

    stateful.set_state(State.FROZEN, True)
    assert (cond | HasState(State.FROZEN)).check(stateful)


def test_condition_not():
    stateful = BasicStatus()
    cond = HasState(State.ON_FIRE)

    assert ~cond.check(stateful)
    assert (~cond).check(stateful)
    assert not (cond & ~cond).check(stateful)
    assert (cond | ~cond).check(stateful)


def test_alive_to_dead():
    stateful = BasicStatus()

    assert IsDead().check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 3)
    assert not IsDead().check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 0)
    assert IsDead().check(stateful)
