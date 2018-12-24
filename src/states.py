"""Abstract implementation of states and conditions."""
from collections import defaultdict
from enum import Enum


class State(Enum):
    """Label for basic state condition requiring no internal logic to check."""
    ON_FIRE = 'on fire'
    FROZEN = 'frozen'

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


