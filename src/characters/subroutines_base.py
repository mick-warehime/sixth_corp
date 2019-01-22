"""Character subroutines."""
import abc
from typing import Any, Tuple

from characters.states import Stateful


class Subroutine(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def _use(self, user: Stateful, target: Stateful) -> None:
        """Internal implementation of use method, must be overridden."""

    @abc.abstractmethod
    def can_use(self, user: Stateful, target: Stateful) -> bool:
        """Whether the subroutine can be used."""

    def use(self, user: Stateful, target: Stateful) -> None:
        assert self.can_use(user, target)
        self._use(user, target)

    @abc.abstractmethod
    def describe_use(self, user: Stateful, target: Stateful) -> str:
        """Description of the subroutine as it was last used."""

    @abc.abstractmethod
    def description(self) -> str:
        """"Description of the subroutine."""

    @property
    def _attrs(self) -> Tuple:
        """Pull out the fields of the concrete class, in alphabetical order.

        This is used for checking (in)equalities below.
        """
        fields = sorted(set(dir(self)) - set(dir(Subroutine)))
        return tuple(self.__getattribute__(f) for f in fields)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self._attrs == other._attrs  # type: ignore

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Subroutine):
            return NotImplemented
        if not isinstance(other, self.__class__):
            return self.__class__.__name__ < other.__class__.__name__
        return self._attrs < other._attrs  # type: ignore
