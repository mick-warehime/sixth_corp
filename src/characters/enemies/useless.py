from typing import Dict, Sequence

from characters.ability_examples import Useless
from characters.chassis import Chassis
from characters.enemies.enemy_builder import EnemyBuilder
from characters.mods_base import GenericMod, Mod
from characters.states import Attribute
from combat.ai.ai_factory import AIType


class UselessBuilder(EnemyBuilder):
    def ai_type(self) -> AIType:
        return AIType.Random

    def initial_mods(self) -> Sequence[Mod]:
        return [GenericMod(abilities_granted=(Useless(1), Useless(2)))]

    def chassis(self) -> Chassis:
        return None

    def additional_attributes(self) -> Dict[Attribute, int]:
        return {}

    def max_health(self) -> int:
        return 1

    def image_path(self) -> str:
        return 'src/images/drone.png'

    def character_name(self) -> str:
        return 'Useless Enemy'
