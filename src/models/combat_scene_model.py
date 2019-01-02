import logging

from models.character_base import Character
from models.player import get_player
from scenes.combat_scene import CombatScene
from models.conditions import IsDead
from models.effects import IncrementAttribute
from events.event_utils import post_scene_change
from scenes.scene_examples import game_over
from models.states import Attribute


class CombatSceneModel(object):

    def __init__(self, scene: CombatScene) -> None:
        self.scene = scene

    def update(self) -> None:
        if self.is_game_over():
            post_scene_change(game_over())
        elif self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()
            logging.debug('Combat scene resolved. Enemy defeated.')
            post_scene_change(resolution.next_scene())

    def is_game_over(self) -> bool:
        return IsDead().check(get_player())

    def _handle_enemy_action(self) -> None:
        action = IncrementAttribute(get_player(), Attribute.HEALTH, -1)
        action.execute()

    def try_player_move(self, index: int) -> None:
        moves = get_player().get_moves(self.scene.enemy())
        if index < len(moves):
            moves[index].use()
            self._handle_enemy_action()

    def enemy(self) -> Character:
        return self.scene.enemy()
