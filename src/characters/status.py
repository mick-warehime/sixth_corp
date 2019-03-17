"""Implementation of  BasicStatus"""
from collections import defaultdict
from typing import Callable, Dict, Tuple, Union

from characters.states import Attributes, AttributeType, State, Status

_BoundFun = Callable[[], int]
_BoundType = Union[int, Attributes, _BoundFun]


class BasicStatus(Status):
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
