from characters.conditions import HasState, IsDead
from characters.states import Attributes, State, Stateful
from characters.status import BasicStatus


class _DummyStateful(Stateful):

    def description(self) -> str:
        return 'dummy stateful'

    @property
    def status(self) -> BasicStatus:
        return self._status

    def __init__(self):
        self._status = BasicStatus()


def test_condition_and():
    stateful = _DummyStateful()

    cond = HasState(State.ON_FIRE) & IsDead()
    assert not cond.check(stateful)
    stateful.status.set_state(State.ON_FIRE, True)
    assert cond.check(stateful)

    assert not (cond & HasState(State.FROZEN)).check(stateful)


def test_condition_or():
    stateful = _DummyStateful()

    cond = HasState(State.ON_FIRE) | IsDead()
    assert cond.check(stateful)
    stateful.status.increment_attribute(Attributes.HEALTH, 1)
    assert not cond.check(stateful)

    stateful.status.set_state(State.FROZEN, True)
    assert (cond | HasState(State.FROZEN)).check(stateful)


def test_condition_not():
    stateful = _DummyStateful()
    cond = HasState(State.ON_FIRE)

    assert ~cond.check(stateful)
    assert (~cond).check(stateful)
    assert not (cond & ~cond).check(stateful)
    assert (cond | ~cond).check(stateful)


def test_alive_to_dead():
    stateful = _DummyStateful()

    assert IsDead().check(stateful)
    stateful.status.increment_attribute(Attributes.HEALTH, 3)
    assert not IsDead().check(stateful)
    stateful.status.increment_attribute(Attributes.HEALTH, -3)
    assert IsDead().check(stateful)
