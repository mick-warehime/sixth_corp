"""Simple example mods."""
from typing import Dict, Sequence

from models.mods_base import Mod
from models.states import AttributeType, State, Attribute, Ability


class HullPlating(Mod):

    def __init__(self, health_bonus=5) -> None:
        self._bonus = health_bonus

    def states_granted(self) -> Sequence[State]:
        return ()

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {Attribute.MAX_HEALTH: self._bonus}


class CamouflagePaint(Mod):

    def __init__(self, sneak_bonus: int = 1) -> None:
        self._bonus = sneak_bonus

    def states_granted(self) -> Sequence[State]:
        return ()

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {Ability.STEALTH: self._bonus}


class HelmOfBeingOnFire(Mod):

    def states_granted(self) -> Sequence[State]:
        return State.ON_FIRE,

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {}
