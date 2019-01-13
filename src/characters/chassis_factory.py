from typing import Union

from characters.chassis import Chassis
from characters.chassis_examples import ChassisData, ChassisTypes
from characters.mods_base import GenericMod


def build_chassis(chassis: Union[ChassisTypes, ChassisData]) -> Chassis:
    if isinstance(chassis, ChassisTypes):
        data = chassis.data
    else:
        data = chassis
    base_mod = GenericMod(data.states_granted, data.attributes_modifiers,
                          data.abilities_granted)
    return Chassis(data.slot_capacities, base_mod)
