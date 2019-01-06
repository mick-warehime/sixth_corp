import abc
from typing import Any

from characters.states import State, Attribute, Stateful


class Condition(metaclass=abc.ABCMeta):
    """Represents a boolean statement that can be tested on Stateful objects.
    """

    @abc.abstractmethod
    def check(self, target: Stateful) -> bool:
        """Evaluate this on a Stateful object to determine condition value."""

    def __and__(self, other: Any) -> '_And':
        if not isinstance(other, Condition):
            return NotImplemented
        return _And(self, other)

    def __or__(self, other: Any) -> '_Or':
        if not isinstance(other, Condition):
            return NotImplemented
        return _Or(self, other)

    def __invert__(self) -> '_Not':
        return _Not(self)


class _And(Condition):
    """Conditional AND of one or more Conditions."""

    def __init__(self, first: Condition, second: Condition) -> None:
        self._conditions = (first, second)

    def check(self, target: Stateful) -> bool:
        return all(c.check(target) for c in self._conditions)


class _Or(Condition):
    """Conditional OR of one or more Conditions."""

    def __init__(self, first: Condition, second: Condition) -> None:
        self._conditions = (first, second)

    def check(self, target: Stateful) -> bool:
        return any(c.check(target) for c in self._conditions)


class _Not(Condition):

    def __init__(self, condition: Condition) -> None:
        self._condition = condition

    def check(self, target: Stateful) -> bool:
        return not self._condition.check(target)


class HasState(Condition):

    def __init__(self, state: State) -> None:
        self._state = state

    def check(self, target: Stateful) -> bool:
        return target.has_state(self._state)


class IsDead(Condition):

    def check(self, target: Stateful) -> bool:
        return not target.get_attribute(Attribute.HEALTH)


class FullHealth(Condition):

    def check(self, target: Stateful) -> bool:
        value = target.get_attribute
        return value(Attribute.HEALTH) == value(Attribute.MAX_HEALTH)
