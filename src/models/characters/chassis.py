"""Implementation of the Chassis"""
import logging
from functools import reduce
from typing import Dict, Iterable, List, NamedTuple, Tuple

from models.characters.inventory import InventoryBase
from models.characters.mods_base import Mod, SlotTypes, build_mod
from models.characters.states import AttributeType, State
from models.characters.subroutines_base import Subroutine


class Chassis(InventoryBase):
    """An inventory which determines storage based on slots."""

    def __init__(self, slot_capacities: Dict[SlotTypes, int],
                 base_mod: Mod = None) -> None:
        """

        Args:
            slot_capacities: How much each slot can hold. If a slot is
                unspecified it is assumed to have zero capacity.
            base_mod: Fixed mod that is granted by the chassis.
        """
        self._slot_capacities: Dict[SlotTypes, int] = slot_capacities.copy()
        self._slot_capacities.update({slot: 0 for slot in SlotTypes
                                      if slot not in slot_capacities})
        self._stored_mods: Dict[SlotTypes, List[Mod]] = {slot: [] for slot in
                                                         SlotTypes}
        self._base_mod = base_mod

    @classmethod
    def from_data(cls, data: 'ChassisData') -> 'Chassis':
        base_mod = build_mod(data.states_granted, data.attribute_modifiers,
                             data.subroutines_granted, description='base mod')
        return Chassis(data.slot_capacities, base_mod)

    @property
    def slot_capacities(self) -> Dict[SlotTypes, int]:
        return self._slot_capacities.copy()

    def mods_in_slot(self, slot: SlotTypes) -> Tuple[Mod, ...]:
        return tuple(self._stored_mods[slot])

    def transfer_mod(self, mod: Mod, target_slot: SlotTypes) -> None:
        """Moves a mod to a specified slot.

        The slot must have sufficient space and be a valid slot for the Mod.
        """
        assert target_slot in mod.valid_slots()
        assert self._slot_vacant(target_slot)

        self.remove_mod(mod)
        logging.debug(
            'Transferring mod {} to {}'.format(mod, target_slot.value))
        self._stored_mods[target_slot].append(mod)

    def can_store(self, mod: Mod) -> bool:
        available_slots = self._open_slots(mod.valid_slots())
        if not available_slots:
            return False
        return all(
            mod not in self._stored_mods[slot] for slot in available_slots)

    def slot_full(self, slot: SlotTypes) -> bool:
        return len(self._stored_mods[slot]) == self._slot_capacities[slot]

    def remove_mod(self, mod: Mod) -> None:
        """Remove a mod from the chassis.

        If the mod is not in the chassis or is the base mod, nothing happens.
        """

        # We don't remove the base mod because it can cause the player's health
        # to go to zero.

        for slot in mod.valid_slots():
            if mod in self._stored_mods[slot]:
                self._stored_mods[slot].remove(mod)
                logging.debug(
                    'INVENTORY: Mod removed from slot {}'.format(slot.value))

    def all_mods(self) -> Iterable[Mod]:
        return self._all_mods(active_only=False)

    def all_active_mods(self) -> Iterable[Mod]:
        return self._all_mods(active_only=True)

    def _all_mods(self, active_only: bool = True) -> Iterable[Mod]:
        # noinspection PyTypeChecker
        checked_slots = set(self._stored_mods.keys())
        if active_only:
            checked_slots.remove(SlotTypes.STORAGE)
        mods = reduce(set.union,  # type: ignore
                      (set(self._stored_mods[slot])
                       for slot in checked_slots))  # type: ignore
        if self._base_mod is not None:
            mods.add(self._base_mod)
        return mods

    def _open_slots(self, slots: Iterable[SlotTypes]) -> List[SlotTypes]:
        return [s for s in slots if self._slot_vacant(s)]

    def _slot_vacant(self, slot: SlotTypes) -> bool:
        return len(self._stored_mods[slot]) < self._slot_capacities[slot]

    def _store(self, mod: Mod) -> None:
        slots_available = self._open_slots(mod.valid_slots())
        active_slots_available = set(slots_available) - {SlotTypes.STORAGE}
        if active_slots_available:
            slot = active_slots_available.pop()
        else:
            slot = SlotTypes.STORAGE

        self._stored_mods[slot].append(mod)
        logging.debug('INVENTORY: Storing mod in slot {}.'.format(slot.value))


class ChassisData(NamedTuple):
    slot_capacities: Dict[SlotTypes, int] = {}
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    subroutines_granted: Tuple[Subroutine, ...] = ()
