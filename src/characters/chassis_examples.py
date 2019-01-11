from enum import Enum

from characters.chassis import Chassis, Slots
from characters.mods_base import GenericMod
from characters.states import State, Attribute, Skill


class Chassises(Enum):
    WALLE = 'WallE'
    DRONE = 'drone'

    def build(self) -> Chassis:
        capacities = _chassis_capacities[self]
        base_mod = GenericMod(_chassis_states[self], _chassis_attributes[self],
                              _chassis_abilities[self])
        return Chassis(capacities, base_mod)

    def __str__(self) -> str:
        return '{} chassis'.format(self.value)


_chassis_capacities = {
    Chassises.WALLE: {Slots.HEAD: 1, Slots.CHEST: 1, Slots.ARMS: 2,
                      Slots.STORAGE: 1},
    Chassises.DRONE: {Slots.HEAD: 1, Slots.STORAGE: 1}
}
_chassis_states = {
    Chassises.WALLE: (),
    Chassises.DRONE: State.ON_FIRE
}
_chassis_attributes = {
    Chassises.WALLE: {Attribute.MAX_HEALTH: 10},
    Chassises.DRONE: {Attribute.MAX_HEALTH: 5}
}
_chassis_abilities = {
    Chassises.WALLE: {Skill.STEALTH: 1, Skill.MECHANICS: 1},
    Chassises.DRONE: {}
}
