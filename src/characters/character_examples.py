"""Data class and examples for enemies."""
from typing import NamedTuple

from characters.chassis_examples import ChassisTypes
from combat.ai.ai_factory import AIType

CharacterData = NamedTuple(
    'EnemyData', [('name', str),
                  ('chassis_type', ChassisTypes),
                  ('image_path', str),
                  ('ai_type', AIType)])

# Sets default values.
CharacterData.__new__.__defaults__ = (  # type: ignore
    'src/images/drone.png', AIType.Random)

DRONE = CharacterData('drone', ChassisTypes.DRONE)  # type: ignore
HARMLESS = CharacterData('harmless enemy',  # type: ignore
                         ChassisTypes.HARMLESS)
USLESS = CharacterData('useless enemy', ChassisTypes.USELESS)  # type: ignore
HUMAN_PLAYER = CharacterData('Player 1', ChassisTypes.WALLE,
                             'src/images/walle.png', AIType.Human)
