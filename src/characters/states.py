"""Abstract implementation of states and conditions."""
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, Tuple, Union


class State(Enum):
    """Label for basic state condition requiring no internal logic to check.

     As a rule, we should define States whose absence is the default.. I.e.,
     ON_FIRE is a good State because Characters are usually not on fire. But
     IS_METALLIC is not good, since most Characters are assumed to be metallic.
     """
    ON_FIRE = 'on fire'
    FROZEN = 'frozen'
    SLEEPY = 'sleepy'

    def __str__(self) -> str:
        return self.value


class Attributes(Enum):
    HEALTH = 'health'
    MAX_HEALTH = 'maximum health'
    CREDITS = 'credits'
    CPU_SLOTS = 'CPU slots'

    def __str__(self) -> str:
        return self.value


class Skill(Enum):
    STEALTH = 'stealth'
    SPEECH = 'speech'
    MECHANICS = 'mechanics'


AttributeType = Union[Attributes, Skill]

_BoundFun = Callable[[], int]
_BoundType = Union[int, Attributes, _BoundFun]


class Stateful(object, metaclass=ABCMeta):
    @abstractmethod
    def has_state(self, state: State) -> bool:
        """Whether object has a given state.

        If not otherwise set, default is False."""

    @abstractmethod
    def get_attribute(self, attribute: AttributeType) -> int:
        """Value associated with an Attribute.

        If not otherwise set, default value is 0."""

    @abstractmethod
    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        """Increment an attribute by a fixed amount."""

    @abstractmethod
    def description(self) -> str:
        """Basic description of the object for logging and display purposes."""


class BasicStatus(Stateful):
    """A Stateful object implemented using simple dictionaries."""

    def __init__(self) -> None:
        self._states: defaultdict = defaultdict(lambda: False)
        self._attributes: defaultdict = defaultdict(lambda: 0)
        self._attribute_bounds: Dict[
            AttributeType, Tuple[_BoundFun, _BoundFun]] = {}

    def has_state(self, state: State) -> bool:
        """Whether object has a given state.

        If not otherwise set, default is False."""
        return self._states[state]

    def set_state(self, state: State, value: bool) -> None:
        self._states[state] = value

    def get_attribute(self, attribute: AttributeType) -> int:
        """Value associated with an Attribute.

        If not otherwise set, default value is 0."""
        return self._attributes[attribute]

    def set_attribute_bounds(
            self, attribute: AttributeType,
            lower: _BoundType,
            upper: _BoundType) -> None:
        if isinstance(lower, int) and isinstance(upper, int):
            assert lower <= upper

        lower = self._parse_bound(lower)
        upper = self._parse_bound(upper)

        self._attribute_bounds[attribute] = (lower, upper)

    def _parse_bound(self, bound: _BoundType) -> _BoundFun:
        if isinstance(bound, int):
            def int_fun() -> int:
                return bound  # type: ignore
        elif isinstance(bound, Attributes):
            def int_fun() -> int:
                return self.get_attribute(bound)  # type: ignore
        else:
            int_fun = bound  # type: ignore

        return int_fun

    def value_in_bounds(self, value: int, attribute: AttributeType) -> int:
        if attribute in self._attribute_bounds:
            lower, upper = self._attribute_bounds[attribute]
            l_val, u_val = lower(), upper()
            assert l_val <= u_val
            value = max(l_val, value)
            value = min(u_val, value)
        return value

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        new_val = self._attributes[attribute] + delta
        new_val = self.value_in_bounds(new_val, attribute)
        self._attributes[attribute] = new_val

    def set_attribute(self, attribute: AttributeType, value: int) -> None:
        value = self.value_in_bounds(value, attribute)
        self._attributes[attribute] = value

    def description(self) -> str:
        return 'BasicStatus'
