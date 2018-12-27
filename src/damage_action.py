from action_base import Action
from character_base import Character
from character_state import State


class DamageAction(Action):

    def __init__(self, magnitude: int) -> None:
        if magnitude <= 0:
            raise ValueError('Damage should >=0, got: {}'.format(magnitude))
        self._magnitude = magnitude

    def apply(self, character: Character) -> None:
        character.update_state(State.HEALTH, -self._magnitude)
