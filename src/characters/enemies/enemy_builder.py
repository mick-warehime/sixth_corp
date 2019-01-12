from abc import abstractmethod
from typing import Any, cast

from characters.character_builder import CharacterBuilder
from characters.enemies.enemy_base import Enemy
from combat.ai.ai_factory import AIType, build_ai


class EnemyBuilder(CharacterBuilder):

    def base_class(self) -> Any:
        return Enemy

    @abstractmethod
    def ai_type(self) -> AIType:
        pass

    def build(self) -> Enemy:
        enemy = cast(Enemy, super().build())
        enemy.ai = build_ai(enemy, self.ai_type())
        enemy.set_position(800, 100, 200, 150)
        return enemy
