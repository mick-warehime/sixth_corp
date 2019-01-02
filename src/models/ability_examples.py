from models.abilities_base import Ability
from models.character_base import Character
from models.conditions import FullHealth
from models.states import Attribute


class Repair(Ability):
    def __init__(self, amount: int):
        assert amount > 0
        self._amount = amount

    def _use(self, user: Character, target: Character) -> None:
        target.increment_attribute(Attribute.HEALTH, self._amount)

    def can_use(self, user: Character, target: Character) -> bool:
        return user == target and not FullHealth().check(target)

    def describe_use(self, user: Character, target: Character) -> str:
        style = 'Repair {} damage.'
        return style.format( self._amount)


class FireLaser(Ability):

    def __init__(self, damage: int) -> None:
        assert damage > 0
        self._damage = damage

    def _use(self, user: Character, target: Character) -> None:
        target.increment_attribute(Attribute.HEALTH, -self._damage)

    def can_use(self, user: Character, target: Character) -> bool:
        return user is not target

    def describe_use(self, user: Character, target: Character) -> str:
        style = 'Fire a laser for {} damage!'
        return style.format(self._damage)
