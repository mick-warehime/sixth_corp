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
    SMALL_LASER = 'small laser'
    BIG_LASER = 'big laser'

    @property
    def data(self) -> ModData:
        return _mod_types_to_data[self]


_mod_types_to_data = {
    ModTypes.BASIC_HULL_PLATING: ModData(
        attribute_modifiers={Attribute.MAX_HEALTH: 3}),
    ModTypes.FIRE_HELM: ModData(states_granted=(State.ON_FIRE,)),
    ModTypes.SLEEPY_AMULET: ModData(states_granted=(State.SLEEPY,)),
    ModTypes.CAMOUFLAGE_PAINT: ModData(attribute_modifiers={Skill.STEALTH: 1}),
    ModTypes.SMALL_LASER: ModData(abilities_granted=(FireLaser(2),)),
    ModTypes.BIG_LASER: ModData(abilities_granted=(FireLaser(4),))

}
