"""Abstract implementation of states and conditions."""
import abc
from collections import defaultdict
from enum import Enum


class State(Enum):
    """Label for basic state condition requiring no internal logic to check."""
    ON_FIRE = 'on fire'
    INANIMATE = 'inanimate'

    def __str__(self):
        return self.value


class Attribute(Enum):
    HEALTH = 'health'
    MAX_HP = 'maximum health'

    def __str__(self):
        return self.value


class Stateful(object):

    def __init__(self):
        self._states = defaultdict(lambda: False)
        self._attributes = defaultdict(lambda: 0)

    def has_state(self, state: State) -> bool:
        """Whether object has a given state.

        If not otherwise set, default is False."""
        return self._states[state]

    def set_state(self, state: State, value: bool) -> None:
        self._states[state] = value

    def get_attribute(self, attribute: Attribute) -> int:
        """Value associated with an Attribute.

        If not otherwise set, default value is 0."""
        return self._attributes[attribute]

    def set_attribute(self, attribute: Attribute, value: int) -> None:
        self._attributes[attribute] = value


class Condition(metaclass=abc.ABCMeta):
    """Represents a boolean statement that can be tested on HasState objects.
    """

    @abc.abstractmethod
    def check(self, target: Stateful) -> bool:
        """Evaluate this on a HasState object to determine condition value."""

    def __and__(self, other):
        if not isinstance(other, Condition):
            return NotImplemented
        return _And(self, other)


class _And(Condition):

    def __init__(self, *conditions: Condition):
        all_conds = set()
        for cond in (c for c in conditions if isinstance(c, _And)):
            all_conds.update(cond._conditions)

        all_conds.update(conditions)
        self._conditions = all_conds

    def check(self, target: Stateful):
        return all(c.check(target) for c in self._conditions)


class HasState(Condition):

    def __init__(self, state: State) -> None:
        self._state = state

    def check(self, target: Stateful):
        return target.has_state(self._state)


class IsDead(Condition):

    @classmethod
    def check(cls, target: Stateful) -> bool:
        return not target.get_attribute(Attribute.HEALTH)
