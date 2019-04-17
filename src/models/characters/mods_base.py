"""Base implementation of mods and inventory."""
import abc
from enum import Enum
from typing import Dict, NamedTuple, Sequence, Set, Tuple, Union

from models.characters.states import AttributeType, State
from models.characters.subroutines_base import Subroutine


class Slots(Enum):
    HEAD = 'head'
    CHEST = 'chest'
    LEGS = 'legs'
    ARMS = 'arms'
    STORAGE = 'storage'


class Mod(metaclass=abc.ABCMeta):
    """Grants state(s) or modifies character attributes."""

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
    def _valid_slots(self) -> Set[Slots]:
        """Slots in which this mod may be stored, excluding STORAGE."""

    def valid_slots(self) -> Set[Slots]:
        """Slots in which this mod may be stored.

        By default, all mods can be stored in the STORAGE slot.
        """
        slots = self._valid_slots().copy()
        slots.add(Slots.STORAGE)
        return slots

    def __str__(self):
        text = 'Mod('
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


class GenericMod(Mod):

    def __init__(
            self, states_granted: Union[State, Sequence[State]] = (),
            attribute_modifiers: Dict[AttributeType, int] = None,
            subroutines_granted: Union[Subroutine, Sequence[Subroutine]] = (),
            valid_slots: Union[Slots, Sequence[Slots]] = Slots.STORAGE) -> None:
        if isinstance(states_granted, State):
            states_granted = states_granted,
        if attribute_modifiers is None:
            attribute_modifiers = {}
        if isinstance(subroutines_granted, Subroutine):
            subroutines_granted = subroutines_granted,
        if isinstance(valid_slots, Slots):
            valid_slots = (valid_slots,)

        self._slots = set(valid_slots)
        self._states = states_granted
        self._attr_mods = attribute_modifiers.copy()
        self._subroutines = subroutines_granted

    def states_granted(self) -> Sequence[State]:
        return self._states

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return self._attr_mods

    def subroutines_granted(self) -> Sequence[Subroutine]:
        return self._subroutines

    def _valid_slots(self) -> Set[Slots]:
        return self._slots


class ModData(NamedTuple):
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    subroutines_granted: Tuple[Subroutine, ...] = ()
    valid_slots: Tuple[Slots, ...] = (Slots.STORAGE,)
