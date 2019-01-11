from enum import Enum
from typing import Dict, Sequence

from characters.abilities_base import Ability
from characters.ability_examples import FireLaser, Repair
from characters.chassis import Chassis, Slots
from characters.mods_base import GenericMod
from characters.states import Attribute, AttributeType, Skill, State


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


_chassis_capacities: Dict[Chassises, Dict[Slots, int]] = {
    Chassises.WALLE: {Slots.HEAD: 1, Slots.CHEST: 1, Slots.ARMS: 2,
                      Slots.STORAGE: 1},
    Chassises.DRONE: {Slots.HEAD: 1, Slots.STORAGE: 1}
}
_chassis_states: Dict[Chassises, Sequence[State]] = {
    Chassises.WALLE: (),
    Chassises.DRONE: (State.ON_FIRE,)
}
_chassis_attributes: Dict[Chassises, Dict[AttributeType, int]] = {
    Chassises.WALLE: {Attribute.MAX_HEALTH: 10,
                      Skill.STEALTH: 1,
                      Skill.MECHANICS: 1},
    Chassises.DRONE: {Attribute.MAX_HEALTH: 5}
}
_chassis_abilities: Dict[Chassises, Sequence[Ability]] = {
    Chassises.WALLE: (FireLaser(2), FireLaser(4), Repair(5)),
    Chassises.DRONE: (FireLaser(2), Repair(1))
}
