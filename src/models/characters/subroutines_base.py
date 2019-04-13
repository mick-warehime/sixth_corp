"""Character subroutines."""
import abc
from functools import partial
from typing import Any, NamedTuple, Callable, Union, cast

from models.characters.character_base import Character


class Subroutine(object):
    """An action that can be taken by a Character object on a Character object.
    """

    def _use(self, user: Character, target: Character) -> None:
        """Internal implementation of use method, must be overridden."""
        pass

    @abc.abstractmethod
    def can_use(self, user: Character, target: Character) -> bool:
        """Whether the subroutine can be used."""
        raise NotImplementedError

    def use(self, user: Character, target: Character) -> None:
        assert self.can_use(user, target)
        self._use(user, target)

    @abc.abstractmethod
    def cpu_slots(self) -> int:
        """Number of CPU slots required for use."""
        raise NotImplementedError

    @abc.abstractmethod
    def time_slots(self) -> int:
        """Number of time slots required before subroutine takes effect."""
        raise NotImplementedError

    @abc.abstractmethod
    def description(self) -> str:
        """"Description of the subroutine."""
        raise NotImplementedError


class _SubroutineImpl(NamedTuple, Subroutine):
    use_fun: Callable[[Character, Character], None]
    can_use_fun: Callable[[Character, Character], bool]
    cpu_slot_fun: Callable[[Character, Character], int]
    time_slot_fun: Callable[[Character, Character], int]
    description_fun: Callable[[Character, Character], str]
    """Concrete generic implementation of Subroutine."""

    def use(self, user: Character, target: Character) -> None:
        assert self.can_use(user, target)
        self.use_fun(user, target)

    def can_use(self, user: Character, target: Character) -> bool:
        return self.can_use_fun(user, target)

    def cpu_slots(self) -> int:
        return self.cpu_slot_fun()

    def time_slots(self) -> int:
        return self.time_slot_fun()

    def description(self) -> str:
        return self.description_fun()


def _do_nothing(user: Character, target: Character) -> None:
    pass


def _can_use_constant(user: Character, target: Character, value: bool) -> bool:
    return value


def _constant(value: Any) -> Any:
    return value


_UseFunType = Union[partial, Callable[[Character, Character], None]]
_CanUseFunType = Union[bool, Callable[[Character, Character], bool], partial]
_DescriptionType = Union[str, Callable[[], str], partial]


def build_subroutine(
        use_fun: _UseFunType = None,
        can_use: _CanUseFunType = True,
        num_cpu: Union[int, Callable[[], int], partial] = 1,
        time_to_resolve: Union[int, Callable[[], int], partial] = 1,
        description: _DescriptionType = 'unnamed subroutine',
) -> Subroutine:
    """Factory function for Subroutines.

    Args:
        use_fun: Function to implement when subroutine is used. If not provided,
            then the subroutine does nothing.
        can_use: Function that determines whether the subroutine can be used
            once it has resolved. A boolean value (True/False) may also be
            specified.
        num_cpu: Number of CPU slots required to load the subroutine onto
            the stack. This may be a non-negative integer or a no-argument
            function that returns an integer.
        time_to_resolve: Rounds required to resolve the subroutine. This may be
            a non-negative integer or a no-argument function that returns an
            integer.
        description: A short string description of the subroutine. This
            may be a string or a no-argument function that returns a string.
    """

    use_fun = _do_nothing if use_fun is None else use_fun

    if isinstance(can_use, bool):
        can_use = partial(_can_use_constant, value=can_use)

    if isinstance(num_cpu, int):
        if num_cpu < 0:
            raise ValueError('non-negative num_cpu only.')
        num_cpu = partial(_constant, value=num_cpu)

    if isinstance(time_to_resolve, int):
        if time_to_resolve < 0:
            raise ValueError('non-negative num_cpu only.')
        time_to_resolve = partial(_constant, value=time_to_resolve)

    if isinstance(description, str):
        description = partial(_constant, value=description)

    return _SubroutineImpl(use_fun, can_use, num_cpu, time_to_resolve,
                           description)
