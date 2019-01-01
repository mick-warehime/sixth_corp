"""Character abilities."""
import abc

from models.character_base import Character
from models.conditions import FullHealth
from models.states import Attribute


class Ability(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def _use(self, user: Character, target: Character) -> None:
        """Internal implementation of use method, must be overridden."""

    @abc.abstractmethod
    def can_use(self, user: Character, target: Character) -> bool:
        """Whether the ability can be used."""

    def use(self, user: Character, target: Character) -> None:
        assert self.can_use(user, target)
        self._use(user, target)

    @abc.abstractmethod
    def describe_use(self, user: Character, target: Character) -> str:
        """Description of use for player."""


class Repair(Ability):
    def __init__(self, amount: int):
        assert amount > 0
        self._amount = amount

    def _use(self, user: Character, target: Character) -> None:
        target.increment_attribute(Attribute.HEALTH, self._amount)

    def can_use(self, user: Character, target: Character) -> bool:
        return not FullHealth().check(target)

    def describe_use(self, user: Character, target: Character) -> str:
        style = '{} repairs {} for {} damage.'
        if user == target:
            return style.format(user, 'itself', self._amount)

        return style.format(user, target, self._amount)


class Laser(Ability):

    def __init__(self, damage: int) -> None:
        assert damage > 0
        self._damage = damage

    def _use(self, user: Character, target: Character) -> None:
        target.increment_attribute(Attribute.HEALTH, -self._damage)

    def can_use(self, user: Character, target: Character) -> bool:
        return user is not target

    def describe_use(self, user: Character, target: Character) -> str:
        style = '{} fires a laser at {} for {} damage!'
        return style.format(user, target, self._damage)
