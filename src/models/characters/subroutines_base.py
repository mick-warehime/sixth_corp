"""Character subroutines."""
import abc
from typing import Any, Tuple

from models.characters.character_base import Character


class Subroutine(metaclass=abc.ABCMeta):
    """An action that can be taken by a Character object on a Character object.
    """

    @abc.abstractmethod
    def _use(self, user: Character, target: Character) -> None:
        """Internal implementation of use method, must be overridden."""

    @abc.abstractmethod
    def can_use(self, user: Character, target: Character) -> bool:
        """Whether the subroutine can be used."""

    def use(self, user: Character, target: Character) -> None:
        assert self.can_use(user, target)
        self._use(user, target)

    @abc.abstractmethod
    def cpu_slots(self) -> int:
        """Number of CPU slots required for use."""

    @abc.abstractmethod
    def time_slots(self) -> int:
        """Number of time slots required before subroutine takes effect."""

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


class _SubroutineImpl(Subroutine):
    """Concrete generic implementation of Subroutine."""

    # def __init__(self):
    #     use_fun: Callable[[Character, Character], None]
    #     can_use_fun: Callable[[Character, Character], bool]
    #     num_cpu_slots: int
    #     time_to_resolve: int
    #     basic_description: str

    def _use(self, user: Character, target: Character) -> None:
        self.use_fun(user, target)

    def can_use(self, user: Character, target: Character) -> bool:
        return self.can_use_fun(user, target)

    def cpu_slots(self) -> int:
        return self.num_cpu_slots

    def time_slots(self) -> int:
        return self.time_to_resolve

    def description(self) -> str:
        return self.basic_description
#
#
# def build_subroutine(use_fun: Callable[[Character, Character], None] = None,
#                      can_use_fun: Callable[[Character, Character], bool] = None,
#                      num_cpu_slots: int = 1,
#                      time_to_resolve: int = 1,
#                      basic_description: str = 'unnamed subroutine',
#                      describe_fun: Callable[[Character, Character], str] = None,
#                      ) -> Subroutine:
#     """Factory method for Subroutines
#
#     Args:
#         use_fun: Function to implement when subroutine is used. If not provided,
#             then the subroutine does nothing.
#         can_use_fun: Function to determine whether the subroutine can be used
#             once it has resolved. If not provided, default is True.
#         num_cpu_slots: Number of CPU slots required to load the subroutine onto
#             the stack.
#         time_to_resolve: Time required to resolve the subroutine.
#         basic_description: A short string description of the subroutine.
#         describe_fun:
#     """
