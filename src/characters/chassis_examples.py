from enum import Enum
from typing import Dict, NamedTuple, Tuple

from characters.abilities_base import Ability
from characters.ability_examples import FireLaser, Harmless, Repair, Useless
from characters.chassis import Slots
from characters.states import Attribute, AttributeType, Skill, State


class ChassisData(NamedTuple):
    slot_capacities: Dict[Slots, int] = {}
    states_granted: Tuple[State, ...] = ()
    attribute_modifiers: Dict[AttributeType, int] = {}
    abilities_granted: Tuple[Ability, ...] = ()


_WALLE = ChassisData(
    slot_capacities={Slots.HEAD: 10, Slots.CHEST: 1, Slots.ARMS: 2,
                     Slots.STORAGE: 1},
    attribute_modifiers={Attribute.MAX_HEALTH: 10, Skill.STEALTH: 1,
                         Skill.MECHANICS: 1},
    abilities_granted=(Repair(5),))

_DRONE = ChassisData(
    slot_capacities={Slots.HEAD: 1, Slots.STORAGE: 1},
    states_granted=(State.ON_FIRE,),
    attribute_modifiers={Attribute.MAX_HEALTH: 5},
    abilities_granted=(FireLaser(2),)
)

_HARMLESS = ChassisData(
    attribute_modifiers={Attribute.MAX_HEALTH: 1},
    abilities_granted=(Harmless(1), Harmless(2), Useless(1), Useless(2))
)

_USELESS = ChassisData(
    attribute_modifiers={Attribute.MAX_HEALTH: 1},
    abilities_granted=(Useless(1), Useless(2))
)


class ChassisTypes(Enum):
    WALLE = 'WallE'
    DRONE = 'drone'
    HARMLESS = 'HARMLESS'
    USELESS = 'USELESS'

    @property
    def data(self) -> ChassisData:
        return _chassis_type_to_data[self]

    def __str__(self) -> str:
        return '{} chassis'.format(self.value)


_chassis_type_to_data: Dict[ChassisTypes, ChassisData] = {
    ChassisTypes.WALLE: _WALLE,
    ChassisTypes.DRONE: _DRONE,
    ChassisTypes.HARMLESS: _HARMLESS,
    ChassisTypes.USELESS: _USELESS}
