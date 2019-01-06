import logging
import random
from collections import Sequence
from typing import List, Tuple

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

    def handle_enemy_action(self) -> None:
        moves = valid_moves(self.enemy(), (self.enemy(), self._player))
        if moves:
            move = random.choice(moves)
            move.use()
        else:
            logging.debug('Enemy has no valid moves, does nothing.')

    def enemy(self) -> Character:
        return self.scene.enemy()


class CombatTargeting(object):
    """Handles targeting of abilities between characters in combat."""

    def __init__(self, user: Character, targets: Sequence) -> None:
        self._user = user
        self._all_targets = targets
        self._selected_ability: Ability = None

    def valid_targets(self) -> Tuple[Character, ...]:
        if self._selected_ability is None:
            return ()
        return tuple(t for t in self._all_targets
                     if self._selected_ability.can_use(self._user, t))

    def select_ability(self, ability: Ability) -> None:
        logging.debug('Selected ability ({})'.format(ability.description()))
        self._selected_ability = ability

    @property
    def selected_ability(self) -> Ability:
        return self._selected_ability

    def abilities_available(self) -> List[Ability]:
        moves = valid_moves(self._user, self._all_targets)
        return sorted({m.ability for m in moves})