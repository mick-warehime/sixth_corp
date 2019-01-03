import logging
from collections import Sequence
from itertools import product
from typing import Tuple, List

from models.abilities_base import Ability
from models.character_base import Character
from models.combat_AI import valid_moves, Move, random_move
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
        logging.debug('Applying player ability ({})'.format(
            ability.describe_use(self._player, target)))
        ability.use(self._player, target)

    def handle_enemy_action(self) -> None:
        move = random_move(self.enemy(), (self.enemy(), self._player))
        move.use()
        logging.debug('Enemy move ({})'.format(move.describe()))

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
