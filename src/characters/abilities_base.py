"""Character abilities."""
import abc
import logging
from typing import Tuple, Any

from characters.states import Stateful


class Ability(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def _use(self, user: Stateful, target: Stateful) -> None:
        """Internal implementation of use method, must be overridden."""

    @abc.abstractmethod
    def can_use(self, user: Stateful, target: Stateful) -> bool:
        """Whether the ability can be used."""

    def use(self, user: Stateful, target: Stateful) -> None:
        assert self.can_use(user, target)
        logging.debug('ABILITY: {}'.format(self.describe_use(user, target)))
        self._use(user, target)

    @abc.abstractmethod
    def describe_use(self, user: Stateful, target: Stateful) -> str:
        """Description of the ability as it was last used."""

    @abc.abstractmethod
    def description(self) -> str:
        """"Description of the ability."""

    @property
    def _attrs(self) -> Tuple:
        """Pull out the fields of the concrete class, in alphabetical order.

        This is used for checking (in)equalities below.
        """
        fields = sorted(set(dir(self)) - set(dir(Ability)))
        return tuple(self.__getattribute__(f) for f in fields)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self._attrs == other._attrs  # type: ignore

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Ability):
            return NotImplemented
        if not isinstance(other, self.__class__):
            return self.__class__.__name__ < other.__class__.__name__
        return self._attrs < other._attrs  # type: ignore

    def __hash__(self) -> int:
        return hash((self.__class__.__name__,) + self._attrs)  # type: ignore
