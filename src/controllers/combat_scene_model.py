import logging
import random

from typing import Sequence

from characters.combat_AI import Move
from combat.combat_manager_base import CombatManager
from characters.abilities_base import Ability
from characters.character_base import Character
from characters.combat_AI import valid_moves
from characters.conditions import IsDead
from characters.player import get_player
from events.event_utils import post_scene_change
from scenes.combat_scene import CombatScene
from scenes.scene_examples import game_over


class CombatSceneModel(object):

    def __init__(self, scene: CombatScene) -> None:
        self.scene = scene
        self._player = get_player()
        self.combat_manager = CombatManager([get_player()], [scene.enemy()])

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
        return IsDead().check(self._player)

    def apply_player_ability(self, ability: Ability,
                             target: Character) -> None:
        ability.use(self._player, target)

    def enemy_action(self) -> Move:
        moves = valid_moves(self.enemy(), (self.enemy(), self._player))
        if len(moves) < 1:
            raise NotImplementedError('Enemy should always have moves')

        return random.choice(moves)

    def enemy(self) -> Character:
        return self.scene.enemy()

    def player_moves(self, target: Character) -> Sequence[Move]:
        if target is None:
            return []
        group_moves = self.combat_manager.attackers_moves()
        # ASSUMING ONLY ONE PLAYER
        moves = [m[0] for m in group_moves]
        return [m for m in moves if m.can_use() and m.target == target]

    def select_player_move(self, move: Move) -> None:
        enemy_move = self.enemy_action()
        self.combat_manager.take_turn([move], [enemy_move])
