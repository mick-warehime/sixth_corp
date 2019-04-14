from enum import Enum
from typing import Dict, NamedTuple, Tuple

from models.characters.mods_base import Slots
from models.characters.states import Attributes, AttributeType, Skill, State
from models.characters.subroutine_examples import repair, direct_damage
from models.characters.subroutines_base import Subroutine, build_subroutine


class ChassisData(NamedTuple):
    slot_capacities: Dict[Slots, int] = {}
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    subroutines_granted: Tuple[Subroutine, ...] = ()


_NO_LEGS = ChassisData(
    slot_capacities={Slots.HEAD: 1, Slots.CHEST: 1, Slots.ARMS: 2,
                     Slots.STORAGE: 10},
    attribute_modifiers={Attributes.MAX_HEALTH: 10, Skill.STEALTH: 1,
                         Skill.MECHANICS: 1, Attributes.CPU_SLOTS: 3},
    subroutines_granted=(repair(5),))

_shoot_laser = direct_damage(2, label='small laser')

_SINGLE_LASER = ChassisData(
    slot_capacities={Slots.HEAD: 1, Slots.STORAGE: 1},
    states_granted=(State.ON_FIRE,),
    attribute_modifiers={Attributes.MAX_HEALTH: 5, Attributes.CPU_SLOTS: 1},
    subroutines_granted=(_shoot_laser,)
)

_do_nothing_1 = build_subroutine(can_use=True, description='Do nothing',
                                 time_to_resolve=1, num_cpu=0)
_do_nothing_2 = build_subroutine(can_use=True, description='Do nothing',
                                 time_to_resolve=2, num_cpu=0)
_unusable = build_subroutine(can_use=False)

_HARMLESS = ChassisData(
    attribute_modifiers={Attributes.MAX_HEALTH: 1, Attributes.CPU_SLOTS: 1},
    subroutines_granted=(_do_nothing_1, _do_nothing_2, _unusable)
)

_USELESS = ChassisData(
    attribute_modifiers={Attributes.MAX_HEALTH: 1, Attributes.CPU_SLOTS: 1},
    subroutines_granted=(_unusable,)
)


class ChassisTypes(Enum):
    NO_LEGS = 'WallE'
    SINGLE_LASER = 'drone'
    HARMLESS = 'HARMLESS'
    USELESS = 'USELESS'

    @property
    def data(self) -> ChassisData:
        return _chassis_type_to_data[self]

    def __str__(self) -> str:
        return '{} chassis'.format(self.value)


_chassis_type_to_data: Dict[ChassisTypes, ChassisData] = {
    ChassisTypes.NO_LEGS: _NO_LEGS,
    ChassisTypes.SINGLE_LASER: _SINGLE_LASER,
    ChassisTypes.HARMLESS: _HARMLESS,
    ChassisTypes.USELESS: _USELESS}
