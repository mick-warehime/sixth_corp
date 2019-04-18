"""Base implementation of mods and inventory."""
import abc
from enum import Enum
from typing import Dict, NamedTuple, Sequence, Set, Tuple, Union

from models.characters.states import AttributeType, State
from models.characters.subroutines_base import Subroutine


class SlotTypes(Enum):
    HEAD = 'head'
    CHEST = 'chest'
    LEGS = 'legs'
    ARMS = 'arms'
    STORAGE = 'storage'


class Mod(metaclass=abc.ABCMeta):
    """Grants state(s) or modifies character attributes."""

    @abc.abstractmethod
    def description(self) -> str:
        """Short text description of mod."""

    @abc.abstractmethod
    def states_granted(self) -> Sequence[State]:
        """The States granted by this mod. """

    @abc.abstractmethod
    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        """Attribute modifiers granted by this mod."""

    @abc.abstractmethod
    def subroutines_granted(self) -> Sequence[Subroutine]:
        """Abilities granted by this mod."""

    @abc.abstractmethod
    def _valid_slots(self) -> Set[SlotTypes]:
        """Slots in which this mod may be stored, excluding STORAGE."""

    def valid_slots(self) -> Set[SlotTypes]:
        """Slots in which this mod may be stored.

        By default, all mods can be stored in the STORAGE slot.
        """
        slots = self._valid_slots().copy()
        slots.add(SlotTypes.STORAGE)
        return slots

    def __str__(self):
        text = 'Mod({}, '.format(self.description())
        text += 'slots: (' + ','.join(s.value for s in self.valid_slots()) + ')'

        if self.states_granted():
            text += ', states: ('
            text += ', '.join(s.value for s in self.states_granted()) + '),'
        if self.attribute_modifiers():
            text += ', attributes: ('
            text += ','.join('{} ({})'.format(att.value, val)
                             for att, val in
                             self.attribute_modifiers().items()) + '),'
        if self.subroutines_granted():
            text += ', subroutines: ('
            text += ','.join(
                sub.description() for sub in self.subroutines_granted())
            text += ')'
        text += ')'

        return text

    __repr__ = __str__


class GenericMod(Mod):

    @classmethod
    def from_data(cls, mod_data: 'ModData') -> 'GenericMod':
        return GenericMod(mod_data.states_granted, mod_data.attribute_modifiers,
                          mod_data.subroutines_granted, mod_data.valid_slots,
                          mod_data.description)

    def __init__(
            self, states_granted: Union[State, Sequence[State]] = (),
            attribute_modifiers: Dict[AttributeType, int] = None,
            subroutines_granted: Union[Subroutine, Sequence[Subroutine]] = (),
            valid_slots: Union[
                SlotTypes, Sequence[SlotTypes]] = SlotTypes.STORAGE,
            description='unnamed mod') -> None:
        if isinstance(states_granted, State):
            states_granted = states_granted,
        if attribute_modifiers is None:
            attribute_modifiers = {}
        if isinstance(subroutines_granted, Subroutine):
            subroutines_granted = (subroutines_granted,)
        if isinstance(valid_slots, SlotTypes):
            valid_slots = (valid_slots,)

        self._slots = set(valid_slots)
        self._states = states_granted
        self._attr_mods = attribute_modifiers.copy()
        self._subroutines = subroutines_granted
        self._description = description

    def states_granted(self) -> Sequence[State]:
        return self._states

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return self._attr_mods

    def subroutines_granted(self) -> Sequence[Subroutine]:
        return self._subroutines

    def description(self):
        return self._description

    def _valid_slots(self) -> Set[SlotTypes]:
        return self._slots


class ModData(NamedTuple):
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    subroutines_granted: Tuple[Subroutine, ...] = ()
    valid_slots: Tuple[SlotTypes, ...] = (SlotTypes.STORAGE,)
    description: str = 'unnamed mod'
