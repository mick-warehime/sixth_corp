"""Basic implementation of character inventory."""
import abc
from typing import Callable, Iterable, Sequence

from characters.mods_base import Mod
from characters.states import AttributeType, State


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

    def grants_state(self, state: State) -> bool:
        return bool(list(self.mods(lambda m: state in m.states_granted())))

    def total_modifier(self, attribute: AttributeType) -> int:
        mods = self.mods(lambda m: attribute in m.attribute_modifiers())
        return sum(m.attribute_modifiers()[attribute] for m in mods)

    def all_abilities(self) -> Sequence['Ability']:
        mods = self.mods(lambda m: bool(m.abilities_granted()))
        abilities = []
        for mod in mods:
            abilities.extend(mod.abilities_granted())
        return sorted(abilities)


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
