"""Basic implementation of character inventory."""
import abc
import logging
from typing import Callable, Iterable, List, Sequence, Tuple

from models.characters.mods_base import Mod
from models.characters.states import AttributeType, State
from models.characters.subroutines_base import Subroutine


def _subroutine_stats(subroutine: Subroutine) -> Tuple[int, int, str]:
    return (subroutine.cpu_slots(), subroutine.time_to_resolve(),
            subroutine.description())


class InventoryBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def can_store(self, mod: Mod) -> bool:
        """Whether a mod can be stored."""

    @abc.abstractmethod
    def _store(self, mod: Mod) -> None:
        """Internal implementation of mod storage.
        """

    def attempt_store(self, mod: Mod) -> None:
        """Store a mod if possible.
        """
        mod_type = mod.__class__.__name__
        if self.can_store(mod):
            logging.debug('{} picking up {}'.format(self, mod_type))
            self._store(mod)
        else:
            logging.debug(
                '{} attempted to pickup {} but was unable.'.format(self,
                                                                   mod_type))

    @abc.abstractmethod
    def remove_mod(self, mod: Mod) -> None:
        """Remove a mod from the inventory."""

    @abc.abstractmethod
    def all_mods(self) -> Iterable[Mod]:
        """Iterate over all mods, including inactive mods."""

    @abc.abstractmethod
    def all_active_mods(self) -> Iterable[Mod]:
        """Iterate over all active mods."""

    def mods(self, check: Callable[[Mod], bool],
             active_only: bool = True) -> Iterable[Mod]:
        """All mods satisfying a given boolean function."""
        if active_only:
            return (m for m in self.all_active_mods() if check(m))
        return (m for m in self.all_mods() if check(m))

    def grants_state(self, state: State) -> bool:
        return bool(list(self.mods(lambda m: state in m.states_granted())))

    def total_modifier(self, attribute: AttributeType) -> int:
        mods = self.mods(lambda m: attribute in m.attribute_modifiers())
        return sum(m.attribute_modifiers()[attribute] for m in mods)

    def all_subroutines(self, active_only: bool = True) -> Sequence[Subroutine]:
        """All subroutines granted by all mods

        Args:
            active_only: Whether to only consider active mods (not in storage
                slot).

        Returns:
            A list of all subroutines sorted by description, cpu slots, and
            time slots.

        """
        mods_with_subroutines = self.mods(
            lambda m: bool(m.subroutines_granted()),
            active_only=active_only)
        subroutines: List[Subroutine] = []
        for mod in mods_with_subroutines:
            subroutines.extend(mod.subroutines_granted())
        return sorted(subroutines, key=_subroutine_stats)


class BasicInventory(InventoryBase):
    """Basic inventory that can store infinite mods.

    A mod can be stored more than once.
    """

    def __init__(self) -> None:
        self._mods: List[Mod] = []

    def can_store(self, mod: Mod) -> bool:
        return True

    def _store(self, mod: Mod) -> None:
        self._mods.append(mod)

    def remove_mod(self, mod: Mod) -> None:
        assert mod in self._mods, 'mod {} not in inventory.'.format(mod)
        self._mods.remove(mod)

    def all_mods(self) -> Iterable[Mod]:
        return (m for m in self._mods)

    all_active_mods = all_mods
