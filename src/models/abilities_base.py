"""Character abilities."""
import abc

from models.character_base import Character


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


