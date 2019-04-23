"""Simple example mods."""
from enum import Enum

from models.characters.mods_base import ModData, SlotTypes
from models.characters.states import Attributes, Skill, State
from models.characters.subroutine_examples import direct_damage, repair, \
    damage_over_time


class ModTypes(Enum):
    BASIC_HULL_PLATING = 'hull plating'
    FIRE_HELM = 'helm of being on fire'
    CAMOUFLAGE_PAINT = 'camo paint'
    SMALL_LASER = 'small laser'
    BIG_LASER = 'big laser'
    LASER_REPEATER = 'laser repeater'
    REPAIR_NANITES = 'self-repair nanites'

    @property
    def data(self) -> ModData:
        return _mod_types_to_data[self]._replace(description=self.value)


_shoot_small = direct_damage(2, label='small laser')
_shoot_big = direct_damage(5, label='big laser')
_shoot_many = damage_over_time(1, time_to_resolve=1, label='laser barrage',
                               duration=3)

_mod_types_to_data = {
    ModTypes.BASIC_HULL_PLATING: ModData(
        attribute_modifiers={Attributes.MAX_HEALTH: 3},
        valid_slots=(SlotTypes.CHEST,)),
    ModTypes.FIRE_HELM: ModData(states_granted=(State.ON_FIRE,),
                                valid_slots=(SlotTypes.HEAD,)),
    ModTypes.CAMOUFLAGE_PAINT: ModData(attribute_modifiers={Skill.STEALTH: 1},
                                       valid_slots=(SlotTypes.CHEST,)),
    ModTypes.SMALL_LASER: ModData(subroutines_granted=(_shoot_small,),
                                  valid_slots=(SlotTypes.ARMS,)),
    ModTypes.BIG_LASER: ModData(subroutines_granted=(_shoot_big,),
                                valid_slots=(SlotTypes.ARMS,)),
    ModTypes.LASER_REPEATER: ModData(subroutines_granted=(_shoot_many,),
                                     valid_slots=(SlotTypes.ARMS,)),
    ModTypes.REPAIR_NANITES: ModData(subroutines_granted=(repair(5),),
                                     valid_slots=(SlotTypes.CHEST,))

}
