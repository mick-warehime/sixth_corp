"""Character subroutines."""
import abc
from functools import partial
from typing import Any, Callable, Union, cast

from models.characters.character_base import Character


class Subroutine(object):
    """An action that can be taken by a Character object on a Character object.

    Intended usage of Subroutines within Moves is handled by the CombatLogic
    class.

    See combat_notes.txt for a summary of combat mechanics.

    """

    def _use(self, user: Character, target: Character) -> None:
        """Internal implementation of use method, must be overridden."""
        pass

    @abc.abstractmethod
    def can_use(self, user: Character, target: Character) -> bool:
        """Whether the subroutine can be used immediately."""
        raise NotImplementedError

    def use(self, user: Character, target: Character) -> None:
        assert self.can_use(user, target)
        self._use(user, target)

    @abc.abstractmethod
    def cpu_slots(self) -> int:
        """Number of CPU slots required for use."""

    @abc.abstractmethod
    def time_to_resolve(self) -> int:
        """Number of rounds required before subroutine takes effect."""

    @abc.abstractmethod
    def duration(self) -> int:
        """Number of rounds over which the subroutine lasts after resolving.
        """

    @abc.abstractmethod
    def multi_use(self) -> bool:
        """Whether the use() method should be invoked multiple rounds.

        If True, then the use() method is invoked when the subroutine resolves,
        then again for duration() more rounds.
        """

    @abc.abstractmethod
    def after_effect(self, user: Character, target: Character) -> None:
        """Function invoked when the subroutine duration expires.

        Specifically, it is invoked d rounds after the subroutine is first used,
        where d = subroutine.duration().
        """

    @abc.abstractmethod
    def description(self) -> str:
        """"Description of the subroutine."""

    @abc.abstractmethod
    def copy(self) -> 'Subroutine':
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
                 duration_fun: Callable[[], int],
                 multi_use_fun: Callable[[], bool],
                 after_effect_fun: Callable[[Character, Character], None]
                 ) -> None:
        self._use_fun = use_fun
        self._can_use_fun = can_use_fun
        self._cpu_slot_fun = cpu_slot_fun
        self._time_slot_fun = time_slot_fun
        self._description_fun = description_fun
        self._duration_fun = duration_fun
        self._multi_use_fun = multi_use_fun
        self._after_effect_fun = after_effect_fun

    def use(self, user: Character, target: Character) -> None:
        self._use_fun(user, target)

    def can_use(self, user: Character, target: Character) -> bool:
        return self._can_use_fun(user, target)

    def cpu_slots(self) -> int:
        return self._cpu_slot_fun()

    def time_to_resolve(self) -> int:
        return self._time_slot_fun()

    def description(self) -> str:
        return self._description_fun()

    def duration(self) -> int:
        return self._duration_fun()

    def multi_use(self) -> bool:
        return self._multi_use_fun()

    def after_effect(self, user: Character, target: Character) -> None:
        self._after_effect_fun(user, target)

    def __copy__(self) -> Subroutine:
        return _SubroutineImpl(self._use_fun, self._can_use_fun,
                               self._cpu_slot_fun, self._time_slot_fun,
                               self._description_fun, self._duration_fun,
                               self._multi_use_fun, self._after_effect_fun)

    copy = __copy__


def _do_nothing(user: Character, target: Character) -> None:
    pass


def _can_use_constant(user: Character, target: Character, value: bool) -> bool:
    return value


def _constant(value: Any) -> Any:
    return value


def build_subroutine(
        use_fun: Callable[[Character, Character], None] = None,
        can_use: Union[bool, Callable[[Character, Character], bool]] = True,
        num_cpu: Union[int, Callable[[], int], partial] = 1,
        time_to_resolve: Union[int, Callable[[], int], partial] = 1,
        description: Union[str, Callable[[], str]] = 'unnamed subroutine',
        duration: Union[int, Callable[[], int]] = 0,
        multi_use: Union[bool, Callable[[], bool]] = False,
        after_effect: Callable[[Character, Character], None] = None
) -> Subroutine:
    """Factory function for Subroutines.

    Args:
        use_fun: Function to implement when subroutine is used. If not provided,
            then the subroutine use() method does nothing.
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
        duration: The number of rounds over which the subroutine use() method is
            invoked.
        multi_use: Whether the use() method should be invoked multiple times.
            This may be a boolean or a no-argument function that returns a
            boolean.
        after_effect: Function invoked when the subroutine duration expires. By
            default no effect occurs.
    """

    use_fun = _do_nothing if use_fun is None else use_fun
    after_effect = _do_nothing if after_effect is None else after_effect

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

    if isinstance(multi_use, bool):
        multi_use = partial(_constant, value=multi_use)

    return cast(Subroutine, _SubroutineImpl(use_fun, can_use, num_cpu,
                                            time_to_resolve, description,
                                            duration, multi_use, after_effect))
