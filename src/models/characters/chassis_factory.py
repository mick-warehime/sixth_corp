from models.characters.chassis import Chassis
from models.characters.chassis_examples import ChassisData
from models.characters.mods_base import GenericMod


def build_chassis(data: ChassisData) -> Chassis:
    base_mod = GenericMod(data.states_granted, data.attribute_modifiers,
                          data.subroutines_granted)
    return Chassis(data.slot_capacities, base_mod)
