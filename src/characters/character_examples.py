"""Data class and examples for enemies."""
from enum import Enum
from typing import NamedTuple

from characters.chassis_examples import ChassisTypes, ChassisData
from combat.ai.ai_factory import AIType

CharacterData = NamedTuple(
    'EnemyData', [('name', str),
                  ('chassis_data', ChassisData),
                  ('image_path', str),
                  ('ai_type', AIType)])

# Sets default values.
CharacterData.__new__.__defaults__ = (  # type: ignore
    'src/images/drone.png', AIType.Random)

_DRONE = CharacterData('drone', ChassisTypes.DRONE.data)  # type: ignore
_HARMLESS = CharacterData('harmless enemy',  # type: ignore
                          ChassisTypes.HARMLESS.data)
_USELESS = CharacterData('useless enemy', # type: ignore
                         ChassisTypes.USELESS.data)
_HUMAN_PLAYER = CharacterData('Player 1', ChassisTypes.WALLE.data,
                              'src/images/walle.png', AIType.Human)


class CharacterTypes(Enum):
    HUMAN_PLAYER = _HUMAN_PLAYER
    DRONE = _DRONE
    HARMLESS = _HARMLESS
    USELESS = _USELESS

    @property
    def data(self) -> CharacterData:
        return self.value
