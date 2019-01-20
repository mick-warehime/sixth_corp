"""Implementation of the Chassis"""
import logging
from functools import reduce
from typing import Dict, Iterable, List

from characters.inventory import InventoryBase
from characters.mods_base import Mod, Slots


class Chassis(InventoryBase):

    def __init__(self, slot_capacities: Dict[Slots, int],
                 base_mod: Mod = None) -> None:
        """

        Args:
            slot_capacities: How much each slot can hold. If a slot is
                unspecified it is assumed to have zero capacity.
            base_mod: Fixed mod that is granted by the chassis.
        """
        self._slot_capacities: Dict[Slots, int] = slot_capacities.copy()
        self._slot_capacities.update({slot: 0 for slot in Slots
                                      if slot not in slot_capacities})
        self._stored_mods: Dict[Slots, List[Mod]] = {slot: [] for slot in Slots}
        self._base_mod = base_mod

    def can_store(self, mod: Mod) -> bool:
        available_slots = self._open_slots(mod.valid_slots())
        if not available_slots:
            return False
        return all(
            mod not in self._stored_mods[slot] for slot in available_slots)

    def _open_slots(self, slots: Iterable[Slots]) -> List[Slots]:
        return [s for s in slots if self._slot_vacant(s)]

    def _slot_vacant(self, slot: Slots) -> bool:
        return len(self._stored_mods[slot]) < self._slot_capacities[slot]

    def _store(self, mod: Mod) -> None:
        slot = self._open_slots(mod.valid_slots())[0]
        self._stored_mods[slot].append(mod)
        logging.debug('INVENTORY: Storing mod in slot {}.'.format(slot.value))

    def remove_mod(self, mod: Mod) -> None:

        for slot in mod.valid_slots():
            if mod in self._stored_mods[slot]:
                self._stored_mods[slot].remove(mod)
                logging.debug(
                    'INVENTORY: Mod removed from slot {}'.format(slot.value))

    def all_mods(self) -> Iterable[Mod]:
        return self._all_mods(active_only=False)

    def _all_mods(self, active_only: bool = True) -> Iterable[Mod]:
        # noinspection PyTypeChecker
        checked_slots = set(self._stored_mods.keys())
        if active_only:
            checked_slots.remove(Slots.STORAGE)
        mods = reduce(set.union,  # type: ignore
                      (set(self._stored_mods[slot])
                       for slot in checked_slots))  # type: ignore
        if self._base_mod is not None:
            mods.add(self._base_mod)
        return mods

    def all_active_mods(self) -> Iterable[Mod]:
        return self._all_mods(active_only=True)
