"""Data class and examples for enemies."""
from enum import Enum
from typing import NamedTuple, Tuple

from models.characters.chassis_examples import ChassisData, ChassisTypes
from models.characters.mod_examples import ModTypes
from models.characters.mods_base import ModData
from models.combat.ai_impl import AIType


class CharacterData(NamedTuple):
    chassis_data: ChassisData
    name: str = 'unnamed Character'
    mods: Tuple[ModData, ...] = ()
    image_path: str = 'src/data/images/drone.png'
    ai_type: AIType = AIType.Random


_DRONE = CharacterData(ChassisTypes.SINGLE_LASER.data, 'drone')
_HARMLESS = CharacterData(ChassisTypes.HARMLESS.data, 'harmless enemy')
_USELESS = CharacterData(ChassisTypes.USELESS.data, 'useless enemy')

_HUMAN_PLAYER = CharacterData(ChassisTypes.NO_LEGS.data, 'Player 1',
                              (ModTypes.SMALL_LASER.data,
                               ModTypes.BIG_LASER.data,
                               ModTypes.BASIC_HULL_PLATING.data),
                              'src/data/images/walle.png', AIType.Human)


class CharacterTypes(Enum):
    HUMAN_PLAYER = _HUMAN_PLAYER
    DRONE = _DRONE
    HARMLESS = _HARMLESS
    USELESS = _USELESS

    @property
    def data(self) -> CharacterData:
        return self.value
