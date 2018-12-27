"""Basic class for player and enemies."""
from character_state import State


class Character(object):

    def __init__(self, health: int) -> None:
        self._attributes = {State.HEALTH: health}

    def has_attribute(self, attr: State) -> bool:
        return attr in self._attributes

    def get_attribute(self, attr: State) -> int:
        return self._attributes[attr]

    def update_attribute(self, attr: State, delta: int) -> None:
        assert self.has_attribute(attr)
        self._attributes[attr] += delta

    def is_alive(self) -> bool:
        return self._attributes[State.HEALTH] > 0
