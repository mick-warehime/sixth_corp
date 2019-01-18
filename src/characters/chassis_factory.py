from characters.chassis import Chassis
from characters.chassis_examples import ChassisData
from characters.mods_base import GenericMod


def build_chassis(data: ChassisData) -> Chassis:
    base_mod = GenericMod(data.states_granted, data.attribute_modifiers,
                          data.abilities_granted)
    return Chassis(data.slot_capacities, base_mod)
