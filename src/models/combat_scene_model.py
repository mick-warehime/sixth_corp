from models.character_base import Character
from scenes.combat_scene import CombatScene
from models.conditions import IsDead
from models.effects import IncrementPlayerAttribute, IncrementAttribute
from events.event_utils import post_scene_change
from scenes.scene_examples import game_over
from models.states import Attribute
from models.world import get_world


class CombatSceneModel(object):

    def __init__(self, scene: CombatScene) -> None:
        self._world = get_world()
        self.scene = scene

    def update(self) -> None:
        if self.is_game_over():
            post_scene_change(game_over())
        elif self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()

            post_scene_change(resolution.next_scene())

    def is_game_over(self) -> bool:
        return IsDead().check(self._world.player)

    def _handle_enemy_action(self) -> None:
        action = IncrementPlayerAttribute(Attribute.HEALTH, -1)
        action.execute()

    def damage_enemy(self, magnitude: int) -> None:
        enemy = self.scene.enemy()
        action = IncrementAttribute(enemy, Attribute.HEALTH, -magnitude)
        action.execute()
        if not IsDead().check(enemy):
            self._handle_enemy_action()

    def player(self) -> Character:
        return self._world.player

    def enemy(self) -> Character:
        return self.scene.enemy()
