from models.characters.conditions import status_condition
from models.characters.states import State, Stateful
from models.characters.status import BasicStatus


class _DummyStateful(Stateful):

    def description(self) -> str:
        return 'dummy stateful'

    @property
    def status(self) -> BasicStatus:
        return self._status

    def __init__(self):
        self._status = BasicStatus()


def test_status_condition_simple():
    on_fire = status_condition(lambda t: t.status.has_state(State.ON_FIRE))

    stateful = _DummyStateful()

    assert not on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, True)

    assert on_fire(stateful)


def test_status_condition_or():
    on_fire = status_condition(lambda t: t.status.has_state(State.ON_FIRE))
    is_sleepy = status_condition(lambda t: t.status.has_state(State.SLEEPY))
    sleepy_or_on_fire = is_sleepy | on_fire

    stateful = _DummyStateful()

    assert not sleepy_or_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, True)

    assert sleepy_or_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, False)
    stateful.status.set_state(State.SLEEPY, True)

    assert sleepy_or_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, True)
    stateful.status.set_state(State.SLEEPY, True)

    assert sleepy_or_on_fire(stateful)


def test_status_condition_and():
    on_fire = status_condition(lambda t: t.status.has_state(State.ON_FIRE))
    is_sleepy = status_condition(lambda t: t.status.has_state(State.SLEEPY))
    sleepy_or_on_fire = is_sleepy & on_fire

    stateful = _DummyStateful()

    assert not sleepy_or_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, True)

    assert not sleepy_or_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, False)
    stateful.status.set_state(State.SLEEPY, True)

    assert not sleepy_or_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, True)
    stateful.status.set_state(State.SLEEPY, True)

    assert sleepy_or_on_fire(stateful)


def test_status_condition_not():
    not_on_fire = ~ status_condition(
        lambda t: t.status.has_state(State.ON_FIRE))

    stateful = _DummyStateful()

    assert not_on_fire(stateful)

    stateful.status.set_state(State.ON_FIRE, True)

    assert not not_on_fire(stateful)
