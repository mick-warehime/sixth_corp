from models.character_base import Character
from models.conditions import IsDead
from typing import Sequence

from scenes.scenes_base import Resolution, Effect, Scene
from models.world import World


class CombatResolution(Resolution):

    @property
    def effects(self) -> Sequence[Effect]:
        return []

    def next_scene(self, world: World) -> Scene:
        from scenes.scene_examples import start_scene
        return start_scene(world)


class CombatScene(Scene):

    def __init__(self) -> None:
        super().__init__()
        self._enemy = Character(health=10)

    def enemy(self) -> Character:
        return self._enemy

    def set_enemy(self, enemy: Character) -> None:
        self._enemy = enemy

    def is_resolved(self) -> bool:
        return IsDead().check(self._enemy)

    def get_resolution(self) -> Resolution:
        return CombatResolution()

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self.enemy()))
