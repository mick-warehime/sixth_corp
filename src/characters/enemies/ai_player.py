from typing import Dict, Sequence

from characters.chassis import Chassis
from characters.enemies.enemy_builder import EnemyBuilder
from characters.mods_base import Mod
from characters.player_builder import PlayerBuilder
from characters.states import Attribute
from combat.ai.ai_factory import AIType


class AIPlayerBuilder(EnemyBuilder):

    def __init__(self, ai_type: AIType = AIType.Random) -> None:
        super().__init__(ai_type)
        self._player_builder = PlayerBuilder()

    def initial_mods(self) -> Sequence[Mod]:
        return self._player_builder.initial_mods()

    def chassis(self) -> Chassis:
        return self._player_builder.chassis()

    def additional_attributes(self) -> Dict[Attribute, int]:
        return self._player_builder.additional_attributes()

    def max_health(self) -> int:
        return self._player_builder.max_health()

    def image_path(self) -> str:
        return self._player_builder.image_path()

    def character_name(self) -> str:
        return self._player_builder.character_name()
