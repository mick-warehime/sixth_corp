"""Base implementation of mods and inventory."""
import abc
from typing import Dict, Sequence, Union

from characters.abilities_base import Ability
from characters.states import AttributeType, State


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


class GenericMod(Mod):

    def __init__(
            self, states_granted: Union[State, Sequence[State]] = (),
            attribute_modifiers: Dict[AttributeType, int] = None,
            abilities_granted: Union[Ability, Sequence[Ability]] = ()) -> None:
        if isinstance(states_granted, State):
            states_granted = states_granted,
        if attribute_modifiers is None:
            attribute_modifiers = {}
        if isinstance(abilities_granted, Ability):
            abilities_granted = abilities_granted,

        self._states = states_granted
        self._attr_mods = attribute_modifiers
        self._abilities = abilities_granted

    def states_granted(self) -> Sequence[State]:
        return self._states

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return self._attr_mods

    def abilities_granted(self) -> Sequence[Ability]:
        return self._abilities
