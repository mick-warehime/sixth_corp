"""Implementation of the Chassis"""
from enum import Enum
from functools import reduce
from typing import Iterable, Dict, List

from characters.inventory import InventoryBase
from characters.mods_base import Mod


class Slots(Enum):
    HEAD = 'head'
    CHEST = 'chest'
    LEGS = 'legs'
    ARMS = 'arms'
    STORAGE = 'storage'


_TEMP_DEFAULT_SLOT = Slots.HEAD


class Chassis(InventoryBase):

    def __init__(self, slot_capacities: Dict[Slots, int]) -> None:
        """

        Args:
            slot_capacities: How much each slot can hold. If a slot is
                unspecified it is assumed to have zero capacity.
        """
        self._slot_capacities: Dict[Slots, int] = slot_capacities.copy()
        self._slot_capacities.update({slot: 0 for slot in Slots
                                      if slot not in slot_capacities})
        self._slots: Dict[Slots, List[Mod]] = {slot: [] for slot in Slots}

    def can_store(self, mod: Mod) -> bool:
        # For now we assume every mod goes on the HEAD slot
        slot = _TEMP_DEFAULT_SLOT
        if len(self._slots[slot]) >= self._slot_capacities[slot]:
            return False
        return mod not in self._slots[slot]

    def _store(self, mod: Mod) -> None:
        slot = _TEMP_DEFAULT_SLOT
        self._slots[slot].append(mod)

    def remove(self, mod: Mod) -> None:
        slot = _TEMP_DEFAULT_SLOT
        if mod in self._slots[slot]:
            self._slots[slot].remove(mod)

    def all_mods(self) -> Iterable[Mod]:
        # noinspection PyTypeChecker
        return reduce(set.union,  # type: ignore
                      (set(slot) for slot in self._slots))  # type: ignore
