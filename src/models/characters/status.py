"""Implementation of  BasicStatus"""
import math
from collections import defaultdict
from functools import reduce
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

from models.characters.states import (Attributes, AttributeType, State, Status,
                                      StatusEffect)

_BoundFun = Callable[[], int]
_BoundType = Optional[Union[int, AttributeType, _BoundFun]]


class BasicStatus(Status):
    """A Stateful object implemented using sets and dictionaries.

    Also included is the ability to set bounds for attributes. This can be
    done by passing numbers, references to other attributes, or no_argument
    functions.

    This implementation also satisfies the contract specified for StatusEffect.
    """

    def __init__(self) -> None:
        self._states: Set[State] = set()
        self._status_effects: List[StatusEffect] = []
        self._states_from_effects: Set[State] = set()
        self._states_prevented: Set[State] = set()
        self._attributes: defaultdict = defaultdict(lambda: 0)
        self._attribute_bounds: Dict[
            AttributeType, Tuple[_BoundFun, _BoundFun]] = {}

    def has_state(self, state: State) -> bool:
        """Whether object has a given state.

        If not otherwise set, default is False."""
        assert not (self._states_from_effects & self._states_prevented)
        return state in self._states or state in self._states_from_effects

    def set_state(self, state: State, value: bool) -> None:
        if state in self._states_prevented or (
                state in self._states_from_effects):
            return  # state cannot be changed

        if value:
            self._states.add(state)
        else:
            self._states.discard(state)

    def get_attribute(self, attribute: AttributeType) -> int:
        """Value associated with an Attribute.

        If not otherwise set, default value is 0."""
        value = self._attributes[attribute]  # base value

        if self._status_effects:
            value += sum(effect.attribute_modifiers.get(attribute, 0)
                         for effect in self._status_effects)
        return self.value_in_bounds(value, attribute)

    def set_attribute_bounds(
            self, attribute: AttributeType,
            lower: _BoundType,
            upper: _BoundType) -> None:
        """Set increment bounds for an attribute.
        """
        if isinstance(lower, int) and isinstance(upper, int):
            assert lower <= upper

        lower = self._parse_bound(lower, True)
        upper = self._parse_bound(upper, False)

        self._attribute_bounds[attribute] = (lower, upper)

    def _parse_bound(self, bound: _BoundType, is_lower: bool) -> _BoundFun:
        if bound is None:
            bound = -math.inf if is_lower else math.inf  # type:ignore

            def int_fun() -> int:
                return bound  # type:ignore
        elif isinstance(bound, int):
            def int_fun() -> int:
                return bound  # type: ignore
        elif isinstance(bound, Attributes):
            def int_fun() -> int:
                return self.get_attribute(bound)  # type: ignore
        else:
            int_fun = bound  # type: ignore

        return int_fun

    def value_in_bounds(self, value: int, attribute: AttributeType) -> int:
        """Bracket a given value within the bounds of a given attribute."""
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

    def _update_effect_states(self) -> None:
        self._states_prevented = reduce(set.union,
                                        (set(eff.states_prevented)
                                         for eff in self._status_effects),
                                        set())
        self._states_from_effects = reduce(set.union,
                                           (set(eff.states_granted) for eff in
                                            self._status_effects), set())
        self._states_from_effects -= self._states_prevented
        self._states -= self._states_prevented

    def add_status_effect(self, effect: StatusEffect) -> None:
        self._status_effects.append(effect)
        self._update_effect_states()

    def remove_status_effect(self, effect: StatusEffect) -> None:
        assert effect in self._status_effects, ('object does not have effect '
                                                '{}'.format(effect))
        self._status_effects.remove(effect)
        self._update_effect_states()

    def active_effects(self, check: Callable[[StatusEffect], bool] = None
                       ) -> Sequence[StatusEffect]:
        if check is None:
            return self._status_effects.copy()
        return [effect for effect in self._status_effects if check(effect)]
