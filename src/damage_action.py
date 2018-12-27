from action_base import Action
from character_base import Character
from states import Attribute


class DamageAction(Action):

    def __init__(self, magnitude: int) -> None:
        if magnitude <= 0:
            raise ValueError('Damage should >=0, got: {}'.format(magnitude))
        self._magnitude = magnitude

    def apply(self, character: Character) -> None:
        character.increment_attribute(Attribute.HEALTH, -self._magnitude)
