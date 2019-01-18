from typing import Sequence

from characters.character_base import Character
from characters.conditions import IsDead
from characters.player import get_player
from combat.combat_manager_base import CombatManager
from combat.moves_base import Move
from combat.moves_factory import valid_moves
from scenes.scenes_base import Effect, Resolution, Scene
from world.world import get_location


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
        self._player = get_player()
        self._enemy: Character = get_location().random_enemy()
        self.combat_manager = CombatManager([self._player], [self._enemy])

        self.selected: Character = None
        self.current_moves: Sequence[str] = None
        self._set_targets()

    def enemy(self) -> Character:
        return self._enemy

    def set_enemy(self, enemy: Character) -> None:
        self._enemy = enemy
        self._set_targets()

    def is_resolved(self) -> bool:
        return IsDead().check(self._enemy)

    def get_resolution(self) -> Resolution:
        return CombatResolution()

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self.enemy()))

    def is_game_over(self) -> bool:
        return IsDead().check(self._player)

    def enemy_action(self) -> Move:
        return self._enemy.select_move()

    def player_moves(self, target: Character) -> Sequence[Move]:
        moves: Sequence[Move] = []
        if target is not None:
            moves = valid_moves(self._player, (target,))
        self.current_moves = moves
        self.selected = target
        return moves

    def select_player_move(self, move: Move) -> None:
        enemy_move = self.enemy_action()
        self.combat_manager.take_turn([move], [enemy_move])

    def _set_targets(self) -> None:
        self._enemy.set_targets([self._player])
