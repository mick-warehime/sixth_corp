from enum import Enum
from typing import Dict

from models.characters.chassis import ChassisData
from models.characters.mods_base import SlotTypes
from models.characters.states import Attributes, Skills, State
from models.characters.subroutine_examples import direct_damage
from models.characters.subroutines_base import build_subroutine

_NO_LEGS = ChassisData(
    slot_capacities={SlotTypes.HEAD: 1, SlotTypes.CHEST: 3, SlotTypes.ARMS: 2,
                     SlotTypes.STORAGE: 10},
    attribute_modifiers={Attributes.MAX_HEALTH: 10, Skills.STEALTH: 1,
                         Skills.MECHANICS: 1, Attributes.MAX_CPU: 4})

_shoot_laser = direct_damage(2, label='small laser')

_SINGLE_LASER = ChassisData(
    slot_capacities={SlotTypes.HEAD: 1, SlotTypes.STORAGE: 1},
    states_granted=(State.ON_FIRE,),
    attribute_modifiers={Attributes.MAX_HEALTH: 5, Attributes.MAX_CPU: 2},
    subroutines_granted=(_shoot_laser,)
)

_do_nothing_1 = build_subroutine(can_use=True, description='Do nothing',
                                 time_to_resolve=1, num_cpu=0)
_do_nothing_2 = build_subroutine(can_use=True, description='Do nothing',
                                 time_to_resolve=2, num_cpu=0)
_unusable = build_subroutine(can_use=False)

_HARMLESS = ChassisData(
    attribute_modifiers={Attributes.MAX_HEALTH: 1, Attributes.MAX_CPU: 1},
    subroutines_granted=(_do_nothing_1, _do_nothing_2, _unusable)
)

_USELESS = ChassisData(
    attribute_modifiers={Attributes.MAX_HEALTH: 1, Attributes.MAX_CPU: 1},
    subroutines_granted=(_unusable,)
)


class ChassisTypes(Enum):
    NO_LEGS = 'WallE'
    DRONE = 'drone'
    HARMLESS = 'HARMLESS'
    USELESS = 'USELESS'

    @property
    def data(self) -> ChassisData:
        return _chassis_type_to_data[self]

    def __str__(self) -> str:
        return '{} chassis'.format(self.value)


_chassis_type_to_data: Dict[ChassisTypes, ChassisData] = {
    ChassisTypes.NO_LEGS: _NO_LEGS,
    ChassisTypes.DRONE: _SINGLE_LASER,
    ChassisTypes.HARMLESS: _HARMLESS,
    ChassisTypes.USELESS: _USELESS}
