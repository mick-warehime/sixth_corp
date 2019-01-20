"""Basic implementation of character inventory."""
import abc
from typing import Callable, Iterable, List, Sequence

from characters.abilities_base import Ability
from characters.mods_base import Mod
from characters.states import AttributeType, State


class InventoryBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def can_store(self, mod: Mod) -> bool:
        """Whether a mod can be stored."""

    @abc.abstractmethod
    def _store(self, mod: Mod) -> None:
        """Internal implementation of mod storage.
        """

    def store(self, mod: Mod) -> None:
        """Store a mod.

        This method fails if can_store is False.
        """
        if not self.can_store(mod):
            raise ValueError('Mod of type {} cannot be stored.'.format(
                mod.__class__.__name__))
        self._store(mod)

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

    def all_abilities(self) -> Sequence[Ability]:
        mods = self.mods(lambda m: bool(m.abilities_granted()))
        abilities: List[Ability] = []
        for mod in mods:
            abilities.extend(mod.abilities_granted())
        return sorted(abilities)


class BasicInventory(InventoryBase):
    """Basic inventory that cans store infinite mods.

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
