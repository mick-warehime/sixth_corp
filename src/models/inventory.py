"""Basic implementation of character inventory."""
import abc
from typing import Iterable, Callable

from models.mods_base import Mod


class InventoryBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def can_store(self, mod: Mod) -> bool:
        """Whether a mod can be stored."""

    @abc.abstractmethod
    def store(self, mod: Mod) -> None:
        """Store a mod.

        can_store should be called first.
        """

    @abc.abstractmethod
    def remove(self, mod: Mod) -> None:
        """Remove a mod from the inventory."""

    @abc.abstractmethod
    def all_mods(self) -> Iterable[Mod]:
        """Iterate over all mods in storage."""

    def mods(self, check: Callable[[Mod], bool]) -> Iterable[Mod]:
        """All mods satisfying a given boolean function."""
        return (m for m in self.all_mods() if check(m))


class BasicInventory(InventoryBase):
    """Basic inventory that cans store infinite mods.

    A mod can be stored more than once.
    """

    def __init__(self):
        self._mods = []

    def can_store(self, mod: Mod) -> bool:
        return True

    def store(self, mod: Mod) -> None:
        self._mods.append(mod)

    def remove(self, mod: Mod) -> None:
        assert mod in self._mods, 'mod {} not in inventory.'.format(mod)
        self._mods.remove(mod)

    def all_mods(self) -> Iterable[Mod]:
        return (m for m in self._mods)
