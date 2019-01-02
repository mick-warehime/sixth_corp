"""Simple example mods."""
from typing import Dict, Sequence

from models.abilities_base import Ability
from models.ability_examples import FireLaser
from models.mods_base import Mod
from models.states import AttributeType, State, Attribute, Skill


class HullPlating(Mod):

    def __init__(self, health_bonus=5) -> None:
        self._bonus = health_bonus

    def states_granted(self) -> Sequence[State]:
        return ()

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {Attribute.MAX_HEALTH: self._bonus}

    def abilities_granted(self) -> Sequence[Ability]:
        return ()


class CamouflagePaint(Mod):

    def __init__(self, sneak_bonus: int = 1) -> None:
        self._bonus = sneak_bonus

    def states_granted(self) -> Sequence[State]:
        return ()

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {Skill.STEALTH: self._bonus}

    def abilities_granted(self) -> Sequence[Ability]:
        return ()


class AmuletOfSleepiness(Mod):

    def states_granted(self) -> Sequence[State]:
        return State.SLEEPY,

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {}

    def abilities_granted(self) -> Sequence[Ability]:
        return ()


class HelmOfBeingOnFire(Mod):

    def states_granted(self) -> Sequence[State]:
        return State.ON_FIRE,

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {}

    def abilities_granted(self) -> Sequence[Ability]:
        return ()


class BasicLaser(Mod):

    def __init__(self, damage=2) -> None:
        self._ability = FireLaser(damage)

    def states_granted(self) -> Sequence[State]:
        return ()

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {}

    def abilities_granted(self) -> Sequence[Ability]:
        return self._ability,


