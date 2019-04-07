from typing import Sequence, Tuple

from models.characters.character_base import Character
from models.characters.conditions import IsDead
from characters.player import get_player
from combat.combat_manager_base import CombatManager
from models.combat.moves_base import Move
from scenes import scene_examples
from scenes.scenes_base import Resolution, Scene
from world.world import get_location


class CombatScene(Scene):

    def __init__(self) -> None:
        super().__init__()
        self._player = get_player()
        self._enemy: Character = get_location().random_enemy()
        self.combat_manager = CombatManager([self._player], [self._enemy])

        self.selected_char: Character = None
        self.current_moves: Sequence[Move] = None
        self._set_targets()

    def characters(self) -> Tuple[Character, ...]:
        return self._player, self._enemy

    def set_enemy(self, enemy: Character) -> None:
        self._enemy = enemy
        self._set_targets()

    def is_resolved(self) -> bool:
        return IsDead().check(self._enemy) or IsDead().check(self._player)

    def get_resolution(self) -> Resolution:
        assert self.is_resolved()
        if IsDead().check(self._enemy):
            return scene_examples.CombatResolution()
        assert IsDead().check(self._player)
        return scene_examples.EndGame()

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self._enemy))

    def player_moves(self, target: Character) -> Sequence[Move]:
        moves: Sequence[Move] = []
        if target is not None:
            moves = self.combat_manager.valid_moves(self._player, (target,))
        self.current_moves = moves
        self.selected_char = target
        return moves

    def select_player_move(self, move: Move) -> None:
        enemy_move = self._enemy.ai.select_move()
        self.combat_manager.take_turn([move], [enemy_move])

    def _set_targets(self) -> None:
        self._enemy.ai.set_targets([self._player])
