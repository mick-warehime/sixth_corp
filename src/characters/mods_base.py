"""Base implementation of mods and inventory."""
import abc
from enum import Enum
from typing import Dict, NamedTuple, Sequence, Set, Tuple, Union

from characters.abilities_base import Ability
from characters.states import AttributeType, State


class Slots(Enum):
    HEAD = 'head'
    CHEST = 'chest'
    LEGS = 'legs'
    ARMS = 'arms'
    STORAGE = 'storage'


TEMP_DEFAULT_SLOT = Slots.STORAGE


class Mod(metaclass=abc.ABCMeta):
    """Grants state(s) or modifies character attributes."""

    @abc.abstractmethod
    def states_granted(self) -> Sequence[State]:
        """The States granted by this mod. """

    @abc.abstractmethod
    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        """Attribute modifiers granted by this mod."""

    @abc.abstractmethod
    def abilities_granted(self) -> Sequence[Ability]:
        """Abilities granted by this mod."""

    @abc.abstractmethod
    def _valid_slots(self) -> Set[Slots]:
        """Slots in which this mod may be stored, excluding STORAGE."""

    def valid_slots(self) -> Set[Slots]:
        """Slots in which this mod may be stored.

        By default, all mods can be stored in the STORAGE slot.
        """
        slots = self._valid_slots().copy()
        slots.add(Slots.STORAGE)
        return slots


class GenericMod(Mod):

    def __init__(
            self, states_granted: Union[State, Sequence[State]] = (),
            attribute_modifiers: Dict[AttributeType, int] = None,
            abilities_granted: Union[Ability, Sequence[Ability]] = (),
            valid_slots: Union[Slots, Sequence[Slots]] = Slots.STORAGE) -> None:
        if isinstance(states_granted, State):
            states_granted = states_granted,
        if attribute_modifiers is None:
            attribute_modifiers = {}
        if isinstance(abilities_granted, Ability):
            abilities_granted = abilities_granted,
        if isinstance(valid_slots, Slots):
            valid_slots = (valid_slots,)

        self._slots = set(valid_slots)
        self._states = states_granted
        self._attr_mods = attribute_modifiers.copy()
        self._abilities = abilities_granted

    def states_granted(self) -> Sequence[State]:
        return self._states

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return self._attr_mods

    def abilities_granted(self) -> Sequence[Ability]:
        return self._abilities

    def _valid_slots(self) -> Set[Slots]:
        return self._slots


class ModData(NamedTuple):
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    abilities_granted: Tuple[Ability, ...] = ()
    valid_slots: Tuple[Slots, ...] = (Slots.STORAGE,)
