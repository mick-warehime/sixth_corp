from character_base import Character
from conditions import IsDead
from effects import Effect
from scenes_base import Resolution
from scenes_base import Scene
from typing import Sequence
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
        self.enemy = Character(health=10)

    def is_resolved(self) -> bool:
        return IsDead().check(self.enemy)

    def get_resolution(self) -> Resolution:
        return CombatResolution()
