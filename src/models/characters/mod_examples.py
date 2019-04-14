"""Simple example mods."""
from enum import Enum

from models.characters.mods_base import ModData, Slots
from models.characters.states import Attributes, Skill, State
from models.characters.subroutine_examples import direct_damage


class ModTypes(Enum):
    BASIC_HULL_PLATING = 'hull plating'
    FIRE_HELM = 'helm of being on fire'
    CAMOUFLAGE_PAINT = 'camo paint'
    SMALL_LASER = 'small laser'
    BIG_LASER = 'big laser'

    @property
    def data(self) -> ModData:
        return _mod_types_to_data[self]


_shoot_small = direct_damage(2, label='small laser')
_shoot_big = direct_damage(5, label='big laser')

_mod_types_to_data = {
    ModTypes.BASIC_HULL_PLATING: ModData(
        attribute_modifiers={Attributes.MAX_HEALTH: 3},
        valid_slots=(Slots.CHEST,)),
    ModTypes.FIRE_HELM: ModData(states_granted=(State.ON_FIRE,),
                                valid_slots=(Slots.HEAD,)),
    ModTypes.CAMOUFLAGE_PAINT: ModData(attribute_modifiers={Skill.STEALTH: 1},
                                       valid_slots=(Slots.CHEST,)),
    ModTypes.SMALL_LASER: ModData(subroutines_granted=(_shoot_small,),
                                  valid_slots=(Slots.ARMS,)),
    ModTypes.BIG_LASER: ModData(subroutines_granted=(_shoot_big,),
                                valid_slots=(Slots.ARMS,))

}
