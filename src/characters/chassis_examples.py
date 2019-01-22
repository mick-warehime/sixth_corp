from enum import Enum
from typing import Dict, NamedTuple, Tuple

from characters.mods_base import Slots
from characters.states import Attributes, AttributeType, Skill, State
from characters.subroutine_examples import FireLaser, Harmless, Repair, Useless
from characters.subroutines_base import Subroutine


class ChassisData(NamedTuple):
    slot_capacities: Dict[Slots, int] = {}
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    subroutines_granted: Tuple[Subroutine, ...] = ()


_NO_LEGS = ChassisData(
    slot_capacities={Slots.HEAD: 1, Slots.CHEST: 1, Slots.ARMS: 2,
                     Slots.STORAGE: 10},
    attribute_modifiers={Attributes.MAX_HEALTH: 10, Skill.STEALTH: 1,
                         Skill.MECHANICS: 1},
    subroutines_granted=(Repair(5),))

_SINGLE_LASER = ChassisData(
    slot_capacities={Slots.HEAD: 1, Slots.STORAGE: 1},
    states_granted=(State.ON_FIRE,),
    attribute_modifiers={Attributes.MAX_HEALTH: 5},
    subroutines_granted=(FireLaser(2),)
)

_HARMLESS = ChassisData(
    attribute_modifiers={Attributes.MAX_HEALTH: 1},
    subroutines_granted=(Harmless(1), Harmless(2), Useless(1), Useless(2))
)

_USELESS = ChassisData(
    attribute_modifiers={Attributes.MAX_HEALTH: 1},
    subroutines_granted=(Useless(1), Useless(2))
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
