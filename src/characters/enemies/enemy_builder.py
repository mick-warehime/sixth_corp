from typing import Any, cast

from characters.character_builder import CharacterBuilder
from characters.enemies.enemy_base import Enemy
from combat.ai.ai_factory import AIType, build_ai


class EnemyBuilder(CharacterBuilder):

    def __init__(self, ai_type: AIType = AIType.Random) -> None:
        self._ai_type = ai_type

    def base_class(self) -> Any:
        return Enemy

    def build(self) -> Enemy:
        enemy = cast(Enemy, super().build())
        enemy.ai = build_ai(enemy, self._ai_type)
        enemy.set_position(800, 300, 200, 150)
        return enemy
