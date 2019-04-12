from functools import reduce
from itertools import product
from typing import List, Optional, Tuple, Sequence

from data.constants import SCREEN_SIZE, BackgroundImages
from events.events_base import (EventListener, EventType, SelectCharacterEvent,
                                SelectPlayerMoveEvent)
from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.conditions import IsDead
from models.characters.player import get_player
from models.combat.combat_stack import CombatStack
from models.combat.moves_base import Move
from models.scenes import scene_examples
from models.scenes.scenes_base import Resolution, Scene
from views.layouts import Layout


def _valid_moves(user: Character, targets: Sequence[Character]) -> List[Move]:
    """All valid moves from a user to a sequence of targets"""
    return [Move(sub, user, target)
            for sub, target in
            product(user.inventory.all_subroutines(), targets)
            if sub.can_use(user, target)]


class CombatScene(EventListener, Scene):

    def __init__(self, enemy: Character = None,
                 win_resolution: Resolution = None,
                 background_image: str = None) -> None:
        if enemy is None:
            enemy = build_character(CharacterTypes.DRONE.data)
        self._enemy: Character = enemy
        super().__init__()
        self._player = get_player()

        self._combat_stack = CombatStack()

        if win_resolution is None:
            win_resolution = scene_examples.ResolutionTypes.RESTART.resolution
        self._win_resolution = win_resolution

        self._selected_char: Character = None

        self._enemy.ai.set_targets([self._player])
        self._layout: Layout = None
        self._update_layout()

        if background_image is None:
            self._background_image = BackgroundImages.CITY.path
        else:
            self._background_image = background_image

    def notify(self, event: EventType) -> None:
        if isinstance(event, SelectCharacterEvent):
            self._selected_char = event.character
        if isinstance(event, SelectPlayerMoveEvent):
            resolved_moves = self._update_stack(event.move)
            for move in resolved_moves:
                move.execute()

    @property
    def combat_stack(self) -> CombatStack:
        return self._combat_stack

    @property
    def selected_char(self) -> Optional[Character]:
        return self._selected_char

    @property
    def layout(self) -> Layout:
        return self._layout

    @property
    def background_image(self) -> str:
        return self._background_image

    def characters(self) -> Tuple[Character, ...]:
        """All characters in the scene.

        The player is always returned first.
        """
        return self._player, self._enemy

    def available_moves(self) -> List[Move]:
        if self._selected_char is None:
            return []
        return _valid_moves(self._player, [self._selected_char])

    def is_resolved(self) -> bool:
        return IsDead().check(self._enemy) or IsDead().check(self._player)

    def get_resolution(self) -> Resolution:
        assert self.is_resolved()
        if IsDead().check(self._enemy):
            return self._win_resolution
        assert IsDead().check(self._player)
        return scene_examples.ResolutionTypes.GAME_OVER.resolution

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self._enemy))

    def _update_stack(self, player_move: Move) -> Tuple[Move]:
        """Update the combat stack according to character actions.

        Time is advanced prior to putting new moves on the stack

        Args:
            player_move: The player's chosen move.

        Returns:
            Tuple of moves that have just resolved, in resolution order.
        """
        self._combat_stack.advance_time()

        enemy_move = self._enemy.ai.select_move()

        self._combat_stack.add_move(player_move,
                                    player_move.subroutine.time_slots())
        self._combat_stack.add_move(enemy_move,
                                    enemy_move.subroutine.time_slots())
        self._update_layout()

        self._selected_char = None
        return self._combat_stack.extract_resolved_moves()

    def _update_layout(self) -> None:
        characters = self.characters()
        # player side layout
        player = characters[0]

        player_layout = Layout([(None, 2), (player, 1), (None, 2)], 'vertical')
        left_column = Layout([(None, 1), (player_layout, 1), (None, 1)],
                             'horizontal')

        # stack layout
        # unresolved moves
        moves_with_time = self.combat_stack.moves_times_remaining()[::-1]
        num_moves = len(moves_with_time)
        unresolved_wgt = max(num_moves, 1)
        elements = []
        for move_and_time in moves_with_time:
            elements.append((move_and_time, 1))
        unresolved = Layout(elements, 'vertical')
        unresolved = Layout([(None, 1), (unresolved, 5), (None, 1)],
                            'horizontal')

        # resolved moves
        resolved_moves = self.combat_stack.extract_resolved_moves()
        resolved_wgt = len(resolved_moves)
        elements = [(mv, 1) for mv in resolved_moves]

        resolved = Layout(elements, 'vertical')
        resolved = Layout([(None, 1), (resolved, 5), (None, 1)], 'horizontal')

        middle_column = Layout([(None, 6), (unresolved, unresolved_wgt),
                                (None, 1), (resolved, resolved_wgt),
                                (None, 6)])

        # enemies layout
        assert len(characters) > 1
        elements = reduce(lambda a, b: a + b,
                          ([(None, 1), (e, 1)] for e in characters[1:]))
        elements.append((None, 1))
        right_column = Layout(elements, 'vertical')

        self._layout = Layout(
            [(left_column, 1), (middle_column, 1), (right_column, 1)],
            'horizontal', SCREEN_SIZE)
