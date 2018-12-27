from character_base import Character
from conditions import IsDead
from typing import Sequence

from scenes_base import Resolution, Effect, Scene
from world import World


class CombatResolution(Resolution):

    @property
    def effects(self) -> Sequence[Effect]:
        return []

    def next_scene(self, world: World) -> Scene:
        from scene_examples import start_scene
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
