from conditions import HasState, IsDead
from states import Stateful, State, Attribute


def test_condition_and():
    stateful = Stateful()

    cond = HasState(State.ON_FIRE) & IsDead()
    assert not cond.check(stateful)
    stateful.set_state(State.ON_FIRE, True)
    assert cond.check(stateful)

    assert not (cond & HasState(State.INANIMATE)).check(stateful)


def test_condition_or():
    stateful = Stateful()

    cond = HasState(State.ON_FIRE) | IsDead()
    assert cond.check(stateful)
    stateful.set_attribute(Attribute.HEALTH, 1)
    assert not cond.check(stateful)

    stateful.set_state(State.INANIMATE, True)
    assert (cond | HasState(State.INANIMATE)).check(stateful)