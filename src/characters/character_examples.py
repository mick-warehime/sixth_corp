"""Data class and examples for enemies."""
from enum import Enum
from typing import NamedTuple, Dict

from characters.character_impl import CharacterImpl
from characters.character_position import Position

from characters.chassis_examples import ChassisTypes
from characters.mods_base import GenericMod
from characters.states import Attribute
from combat.ai.ai_factory import AIType, build_ai

CharacterData = NamedTuple(
    'EnemyData', [('name', str),
                  ('chassis_type', ChassisTypes),
                  ('image_path', str),
                  ('ai_type', AIType)])

# Sets default values.
CharacterData.__new__.__defaults__ = (  # type: ignore
    'src/images/drone.png', AIType.Random)

_DRONE = CharacterData('drone', ChassisTypes.DRONE)  # type: ignore
_HARMLESS = CharacterData('harmless enemy',  # type: ignore
                          ChassisTypes.HARMLESS)
_USELESS = CharacterData('useless enemy', ChassisTypes.USELESS)  # type: ignore
_HUMAN_PLAYER = CharacterData('Player 1', ChassisTypes.WALLE,
                              'src/images/walle.png', AIType.Human)


class CharacterTypes(Enum):
    HUMAN_PLAYER = _HUMAN_PLAYER
    DRONE = _DRONE
    HARMLESS = _HARMLESS
    USELESS = _USELESS

    def build(self) -> CharacterImpl:
        data = self.value

        # This is an intermediate fix as in future these things will be handled
        # by the chassis.
        chassis = data.chassis_type.build()
        max_health = chassis.total_modifier(Attribute.MAX_HEALTH)

        char = CharacterImpl(health=max_health,
                             image_path=data.image_path,
                             name=data.name)

        temp_mod = GenericMod(abilities_granted=chassis.all_abilities())
        char.attempt_pickup(temp_mod)

        # TODO(#112) - move positions to combat view
        if self == CharacterTypes.HUMAN_PLAYER:
            pos = Position(200, 500, 150, 150)
        else:
            pos = Position(800, 300, 200, 150)
        char.position = pos
        char.ai = build_ai(char, data.ai_type)

        return char
