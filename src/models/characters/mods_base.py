"""Base implementation of mods and inventory."""
import abc
from enum import Enum
from typing import Dict, List, NamedTuple, Sequence, Set, Tuple, Union

from models.characters.states import AttributeType, State
from models.characters.subroutines_base import Subroutine


class SlotTypes(Enum):
    HEAD = 'head'
    CHEST = 'chest'
    LEGS = 'legs'
    ARMS = 'arms'
    STORAGE = 'storage'  # A default slot for storing inactive mods.
    GROUND = 'ground'  # A default slot that should not be in a Chassis.


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
        """Subroutines granted by this mod. """

    @abc.abstractmethod
    def _valid_slots(self) -> Set[SlotTypes]:
        """Slots in which this mod may be stored, excluding STORAGE."""

    def valid_slots(self) -> List[SlotTypes]:
        """Slots in which this mod may be stored.

        By default, all mods can be stored in the STORAGE slot.
        """
        slots = [s for s in SlotTypes if s in self._valid_slots()]
        slots.append(SlotTypes.STORAGE)
        return slots

    def __str__(self) -> str:
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


class _ModImpl(Mod):

    def __init__(
            self, states_granted: Tuple[State, ...] = (),
            attribute_modifiers: Dict[AttributeType, int] = None,
            subroutines_granted: Tuple[Subroutine, ...] = (),
            valid_slots: Tuple[SlotTypes, ...] = (),
            description: str = 'unnamed mod') -> None:
        self._slots = set(valid_slots)
        self._states = states_granted
        if attribute_modifiers is None:
            attribute_modifiers = {}
        self._attr_mods = attribute_modifiers.copy()
        self._subroutines = subroutines_granted
        self._description = description

    def states_granted(self) -> Sequence[State]:
        return self._states

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return self._attr_mods

    def subroutines_granted(self) -> Sequence[Subroutine]:
        return self._subroutines

    def description(self) -> str:
        return self._description

    def _valid_slots(self) -> Set[SlotTypes]:
        return self._slots


class ModData(NamedTuple):
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    subroutines_granted: Tuple[Subroutine, ...] = ()
    valid_slots: Tuple[SlotTypes, ...] = ()
    description: str = 'unnamed mod'


_SubsType = Union[Subroutine, Sequence[Subroutine]]


def build_mod(states_granted: Union[State, Sequence[State]] = (),
              attribute_modifiers: Dict[AttributeType, int] = None,
              subroutines_granted: _SubsType = (),
              valid_slots: Union[
                  SlotTypes, Sequence[SlotTypes]] = SlotTypes.STORAGE,
              description: str = 'unnamed mod',
              data: ModData = None) -> Mod:
    """Factory function for Mods.

    Args:
        states_granted: [Optional] The states granted by the Mod, when active.
            Can be a single state or sequence of states.
        attribute_modifiers: [Optional] Dictionary of attribute (or skill)
            modifiers.
        subroutines_granted: [Optional] The subroutines granted by the Mod, when
            active. Can be a single subroutine or sequence of subroutines.
        valid_slots: [Optional] slot or slots where the mod can be stored. All
            mods can be stored in the STORAGE slot so this slot need not be
            specified.
        description: [Optional] Short string description of the mod. This is
            used in the inventory scene.
        data: [Optional] A ModData object encoding the mod properties. If this
            is passed, all other arguments are ignored.
    """

    if data is not None:
        return build_mod(data.states_granted, data.attribute_modifiers,
                         data.subroutines_granted, data.valid_slots,
                         data.description)

    # Parse inputs to standard form
    if isinstance(states_granted, State):
        states_granted = states_granted,
    if attribute_modifiers is None:
        attribute_modifiers = {}
    if isinstance(subroutines_granted, Subroutine):
        subroutines_granted = (subroutines_granted,)
    if isinstance(valid_slots, SlotTypes):
        valid_slots = (valid_slots,)

    return _ModImpl(tuple(states_granted), attribute_modifiers,
                    tuple(subroutines_granted), tuple(valid_slots), description)
