from conditions import HasState, IsDead
from states import Stateful, State


def test_condition_and():
    stateful = Stateful()

    cond = HasState(State.ON_FIRE) & IsDead()
    assert not cond.check(stateful)
    stateful.set_state(State.ON_FIRE, True)
    assert cond.check(stateful)

    assert not (cond & HasState(State.INANIMATE)).check(stateful)