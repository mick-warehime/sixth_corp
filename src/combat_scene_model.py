from character_base import Character
from combat_scene import CombatScene
from conditions import IsDead
from damage_action import DamageAction
from events_utils import post_scene_change
from scene_examples import game_over
from world import World


class CombatSceneModel(object):

    def __init__(self, world: World, scene: CombatScene) -> None:
        self.world = world
        self.scene = scene

    def update(self) -> None:
        if self.is_game_over():
            post_scene_change(game_over(self.world))
        elif self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute(self.world)

            post_scene_change(resolution.next_scene(self.world))

    def is_game_over(self) -> bool:
        return IsDead().check(self.world.player)

    def _handle_enemy_action(self) -> None:
        action = DamageAction(1)
        action.apply(self.world.player)

    def damage_enemy(self, magnitude: int) -> None:
        action = DamageAction(magnitude=magnitude)
        enemy = self.scene.enemy()
        action.apply(enemy)
        if not IsDead().check(enemy):
            self._handle_enemy_action()

    def player(self) -> Character:
        return self.world.player

    def enemy(self) -> Character:
        return self.scene.enemy()
