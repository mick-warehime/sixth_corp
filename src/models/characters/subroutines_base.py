"""Character subroutines."""
import abc
from functools import partial
from typing import Any, Callable, Union, cast

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

    @abc.abstractmethod
    def time_slots(self) -> int:
        """Number of time slots required before subroutine takes effect."""

    @abc.abstractmethod
    def duration(self) -> int:
        """The number of rounds over which the subroutine use method is invoked.
        """

    @abc.abstractmethod
    def description(self) -> str:
        """"Description of the subroutine."""

    @abc.abstractmethod
    def copy(self)->'Subroutine':
        """Return a copy of the subroutine.

        Copies are not identified as equal, i.e.
        subroutine.copy() != subroutine.
        """


class _SubroutineImpl(Subroutine):
    """Concrete generic implementation of Subroutine."""

    def __init__(self, use_fun: Callable[[Character, Character], None],
                 can_use_fun: Callable[[Character, Character], bool],
                 cpu_slot_fun: Callable[[], int],
                 time_slot_fun: Callable[[], int],
                 description_fun: Callable[[], str],
                 duration_fun: Callable[[], int]) -> None:
        self._use_fun = use_fun
        self._can_use_fun = can_use_fun
        self._cpu_slot_fun = cpu_slot_fun
        self._time_slot_fun = time_slot_fun
        self._description_fun = description_fun
        self._duration = duration_fun

    def use(self, user: Character, target: Character) -> None:
        assert self.can_use(user, target)
        self._use_fun(user, target)

    def can_use(self, user: Character, target: Character) -> bool:
        return self._can_use_fun(user, target)

    def cpu_slots(self) -> int:
        return self._cpu_slot_fun()

    def time_slots(self) -> int:
        return self._time_slot_fun()

    def description(self) -> str:
        return self._description_fun()

    def duration(self) -> int:
        return self._duration()

    def __copy__(self) -> Subroutine:
        return _SubroutineImpl(self._use_fun, self._can_use_fun,
                               self._cpu_slot_fun, self._time_slot_fun,
                               self._description_fun, self._duration)

    copy = __copy__


def _do_nothing(user: Character, target: Character) -> None:
    pass


def _can_use_constant(user: Character, target: Character, value: bool) -> bool:
    return value


def _constant(value: Any) -> Any:
    return value


def build_subroutine(
        use_fun: Union[Callable[[Character, Character], None]] = None,
        can_use: Union[bool, Callable[[Character, Character], bool]] = True,
        num_cpu: Union[int, Callable[[], int], partial] = 1,
        time_to_resolve: Union[int, Callable[[], int], partial] = 1,
        description: Union[str, Callable[[], str]] = 'unnamed subroutine',
        duration: Union[int, Callable[[], int]] = 1,
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
        duration: The number of rounds over which the subroutine use method is
            invoked.
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

    if isinstance(duration, int):
        duration = partial(_constant, value=duration)

    return cast(Subroutine, _SubroutineImpl(use_fun, can_use, num_cpu,
                                            time_to_resolve, description,
                                            duration))
