from enum import Enum
from typing import Dict, NamedTuple, Optional, Tuple

from characters.abilities_base import Ability
from characters.ability_examples import FireLaser, Repair, Harmless, Useless
from characters.chassis import Chassis, Slots
from characters.mods_base import GenericMod
from characters.states import Attribute, AttributeType, Skill, State


class ChassisTypes(Enum):
    WALLE = 'WallE'
    DRONE = 'drone'
    HARMLESS = 'HARMLESS'
    USELESS = 'USELESS'

    def build(self) -> Chassis:
        data = _chassis_type_to_data[self]
        base_mod = GenericMod(data.states_granted, data.attributes_modifiers,
                              data.abilities_granted)
        return Chassis(data.slot_capacities, base_mod)

    def __str__(self) -> str:
        return '{} chassis'.format(self.value)


ChassisData = NamedTuple(
    'ChassisData',
    [('slot_capacities', Dict[Slots, int]),
     ('states_granted', Optional[Tuple[State, ...]]),
     ('attributes_modifiers', Optional[Dict[AttributeType, int]]),
     ('abilities_granted', Optional[Tuple[Ability, ...]])])

# This sets default values.
# I realize that {} is mutable, but I don't want to have to install the package
# frozendict just for this.
ChassisData.__new__.__defaults__ = ({}, (), {}, ())  # type: ignore

_WALLE = ChassisData(  # type: ignore
    slot_capacities={Slots.HEAD: 1, Slots.CHEST: 1, Slots.ARMS: 2,
                     Slots.STORAGE: 1},
    attributes_modifiers={Attribute.MAX_HEALTH: 10, Skill.STEALTH: 1,
                          Skill.MECHANICS: 1},
    abilities_granted=(FireLaser(2), FireLaser(4), Repair(5)))

_DRONE = ChassisData(
    slot_capacities={Slots.HEAD: 1, Slots.STORAGE: 1},
    states_granted=(State.ON_FIRE,),
    attributes_modifiers={Attribute.MAX_HEALTH: 5},
    abilities_granted=(FireLaser(2),)
)

_HARMLESS = ChassisData(  # type:ignore
    attributes_modifiers={Attribute.MAX_HEALTH: 1},
    abilities_granted=(Harmless(1), Harmless(2), Useless(1), Useless(2))
)

_USELESS = ChassisData(  # type:ignore
    attributes_modifiers={Attribute.MAX_HEALTH: 1},
    abilities_granted=(Useless(1), Useless(2))
)

_chassis_type_to_data: Dict[ChassisTypes, ChassisData] = {
    ChassisTypes.WALLE: _WALLE,
    ChassisTypes.DRONE: _DRONE,
    ChassisTypes.HARMLESS: _HARMLESS,
    ChassisTypes.USELESS: _USELESS}
