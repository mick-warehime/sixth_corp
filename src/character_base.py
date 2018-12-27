"""Basic class for player and enemies."""
from character_state import State


class Character(object):

    def __init__(self, health: int) -> None:
        self._states = {State.HEALTH: health}

    def has_state(self, attr: State) -> bool:
        return attr in self._states

    def get_state(self, attr: State) -> int:
        return self._states[attr]

    def update_state(self, attr: State, delta: int) -> None:
        assert self.has_state(attr)
        self._states[attr] += delta

    def is_alive(self) -> bool:
        return self._states[State.HEALTH] > 0
