from characters.ability_examples import FireLaser
from characters.character_base import Character
from characters.enemy_base import Enemy
from characters.conditions import IsDead
from typing import Sequence

from characters.mods_base import GenericMod
from scenes.scenes_base import Resolution, Effect, Scene


class CombatResolution(Resolution):

    @property
    def effects(self) -> Sequence[Effect]:
        return []

    def next_scene(self) -> Scene:
        from scenes.scene_examples import start_scene
        return start_scene()


class CombatScene(Scene):

    def __init__(self) -> None:
        super().__init__()
        self._enemy = Enemy(health=10, name='troll')
        self._enemy.attempt_pickup(GenericMod(abilities_granted=FireLaser(2)))

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
