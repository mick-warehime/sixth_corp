import logging
from itertools import product
from typing import Tuple, List

from models.abilities_base import Ability
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
        self._selected_ability: Ability = None
        self._all_targets = (get_player(), scene.enemy())

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

    def usable_abilities(self) -> List[Ability]:
        player = get_player()
        return [a for a in player.abilities()
                if any(a.can_use(player, t) for t in self._all_targets)]

    def select_ability(self, index: int) -> None:
        ability = get_player().abilities()[index]
        logging.debug('Selected ability ({})'.format(ability.description()))
        self._selected_ability = ability

    def valid_targets(self) -> Tuple[Character, ...]:
        if self._selected_ability is None:
            return ()
        return tuple(t for t in self._all_targets
                     if self._selected_ability.can_use(get_player(), t))

    def apply_player_ability(self, target_index) -> None:
        target = self.valid_targets()[target_index]
        self._selected_ability.use(get_player(), target)

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
