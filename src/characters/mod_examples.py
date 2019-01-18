"""Simple example mods."""
from enum import Enum
from typing import Dict, Sequence

from characters.abilities_base import Ability
from characters.ability_examples import FireLaser
from characters.mods_base import Mod, ModData
from characters.states import Attribute, AttributeType, Skill, State


class ModTypes(Enum):
    BASIC_HULL_PLATING = 'hull plating'
    FIRE_HELM = 'helm of being on fire'
    SLEEPY_AMULET = 'amulet of sleepiness'
    CAMOUFLAGE_PAINT = 'camo paint'

    @property
    def data(self) -> ModData:
        return _mod_types_to_data[self]


class HullPlating(Mod):

    def __init__(self, health_bonus: int = 5) -> None:
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

    def __init__(self, damage: int = 2) -> None:
        self._ability = FireLaser(damage)

    def states_granted(self) -> Sequence[State]:
        return ()

    def attribute_modifiers(self) -> Dict[AttributeType, int]:
        return {}

    def abilities_granted(self) -> Sequence[Ability]:
        return self._ability,


_mod_types_to_data = {
    ModTypes.BASIC_HULL_PLATING: ModData(
        attribute_modifiers={Attribute.MAX_HEALTH: 3}),
    ModTypes.FIRE_HELM: ModData(states_granted=(State.ON_FIRE,)),
    ModTypes.SLEEPY_AMULET: ModData(states_granted=(State.SLEEPY,)),
    ModTypes.CAMOUFLAGE_PAINT: ModData(attribute_modifiers={Skill.STEALTH: 1})

}
