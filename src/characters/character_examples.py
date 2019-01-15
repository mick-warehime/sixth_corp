"""Data class and examples for enemies."""
from enum import Enum
from typing import NamedTuple, Tuple

from characters.ability_examples import FireLaser
from characters.chassis_examples import ChassisData, ChassisTypes
from characters.mods_factory import ModData
from combat.ai_factory import AIType

CharacterData = NamedTuple(
    'EnemyData', [('chassis_data', ChassisData),
                  ('name', str),
                  ('mods', Tuple[ModData, ...]),
                  ('image_path', str),
                  ('ai_type', AIType)])

# Sets default values.
CharacterData.__new__.__defaults__ = ('', (),  # type: ignore
                                      'src/images/drone.png', AIType.Random)

_DRONE = CharacterData(ChassisTypes.DRONE.data, 'drone')  # type: ignore
_HARMLESS = CharacterData(ChassisTypes.HARMLESS.data,  # type: ignore
                          'harmless enemy')
_USELESS = CharacterData(ChassisTypes.USELESS.data,  # type: ignore
                         'useless enemy')

small_laser = ModData(abilities_granted=(FireLaser(2),))  # type: ignore
big_laser = ModData(abilities_granted=(FireLaser(4),))  # type: ignore
_HUMAN_PLAYER = CharacterData(ChassisTypes.WALLE.data, 'Player 1',
                              (small_laser, big_laser),
                              'src/images/walle.png', AIType.Human)


class CharacterTypes(Enum):
    HUMAN_PLAYER = _HUMAN_PLAYER
    DRONE = _DRONE
    HARMLESS = _HARMLESS
    USELESS = _USELESS

    @property
    def data(self) -> CharacterData:
        return self.value
