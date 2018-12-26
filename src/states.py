"""Abstract implementation of states and conditions."""
from collections import defaultdict, Callable
from enum import Enum
from typing import Union


class State(Enum):
    """Label for basic state condition requiring no internal logic to check."""
    ON_FIRE = 'on fire'
    FROZEN = 'frozen'

    def __str__(self):
        return self.value


class Attribute(Enum):
    HEALTH = 'health'
    MAX_HEALTH = 'maximum health'

    def __str__(self):
        return self.value


_BoundType = 'Union[int, Callable[[Stateful], int]]'


class Stateful(object):

    def __init__(self):
        self._states = defaultdict(lambda: False)
        self._attributes = defaultdict(lambda: 0)
        self._attribute_bounds = {}

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

    def set_attribute_bounds(
            self, attribute: Attribute,
            lower: _BoundType,
            upper: _BoundType) -> None:
        if isinstance(lower, int) and isinstance(upper, int):
            assert lower <= upper

        lower = self._parse_bound(lower)
        upper = self._parse_bound(upper)

        self._attribute_bounds[attribute] = (lower, upper)

    def _parse_bound(self,
                     num_or_fun: _BoundType) -> 'Callable[[Stateful], int]':
        if not isinstance(num_or_fun, int):
            return num_or_fun
        value = num_or_fun

        def int_fun(x: Stateful):
            return value

        return int_fun

    def _check_attribute_bounds(self, attribute: Attribute):
        if attribute in self._attribute_bounds:
            value = self._attributes[attribute]
            lower, upper = self._attribute_bounds[attribute]
            lower, upper = lower(self), upper(self)
            assert lower <= upper
            value = max(lower, value)
            value = min(upper, value)
            self._attributes[attribute] = value

    def increment_attribute(self, attribute: Attribute, delta: int) -> None:
        self._attributes[attribute] += delta
        self._check_attribute_bounds(attribute)

    def set_attribute(self, attribute: Attribute, value: int) -> None:
        self._attributes[attribute] = value
        self._check_attribute_bounds(attribute)
