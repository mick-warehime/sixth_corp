from functools import reduce
from itertools import product
from typing import List, Optional, Sequence, Tuple

from data.constants import SCREEN_SIZE, BackgroundImages, FRAMES_PER_SECOND
from events.events_base import (EventListener, EventType, SelectCharacterEvent,
                                SelectPlayerMoveEvent, BasicEvents)
from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.conditions import IsDead
from models.characters.player import get_player
from models.characters.subroutines_base import build_subroutine
from models.combat.combat_stack import CombatStack
from models.combat.moves_base import Move
from models.scenes import scene_examples
from models.scenes.scenes_base import Resolution, Scene
from views.layouts import Layout

_wait_one_round = build_subroutine(can_use=True, num_cpu=0, time_to_resolve=1,
                                   description='wait one round')

_ANIMATION_TIME_SECONDS = 1.0
_ticks_per_animation = FRAMES_PER_SECOND * _ANIMATION_TIME_SECONDS
ANIMATION = True  # Set to False during integration tests


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

        self._animation_progress: float = None
        self._first_turn = True

    def notify(self, event: EventType) -> None:
        if isinstance(event, SelectCharacterEvent):
            self._selected_char = event.character
        if isinstance(event, SelectPlayerMoveEvent):
            self._update_stack(event.move)

            # If animation enabled, start progress. Otherwise execute moves.
            if ANIMATION and not self._first_turn:
                self._animation_progress = 0.0
            else:
                for move in self.combat_stack.extract_resolved_moves():
                    move.execute()
            self._first_turn = False

        # Animation in progress
        if event == BasicEvents.TICK and self.animation_progress is not None:
            self._animation_progress += 1.0 / _ticks_per_animation
            # Execute moves once animation is finished
            if self._animation_progress >= 1.0:
                self._animation_progress = None
                for move in self.combat_stack.extract_resolved_moves():
                    move.execute()

    @property
    def animation_progress(self) -> Optional[float]:
        """Progress of a combat scene animation.

        This variable is None if no animation is in progress.
        """
        return self._animation_progress

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
            return [Move(_wait_one_round, self._player, self._player)]
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

    def _update_stack(self, player_move: Move) -> None:
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
        # return self._combat_stack.extract_resolved_moves()

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
        stack_size = 6
        move_time_elements = []
        for move_and_time in moves_with_time:
            move_time_elements.append((move_and_time, 1))
        if num_moves <= stack_size:
            move_time_elements.append((None, stack_size - num_moves))

        unresolved = Layout(move_time_elements, 'vertical')
        unresolved = Layout([(None, 1), (unresolved, 5), (None, 1)],
                            'horizontal')

        # resolved moves
        resolved_size = 4
        resolved_moves = self.combat_stack.extract_resolved_moves()[::-1]
        move_elements = [(mv, 1) for mv in resolved_moves]
        if len(resolved_moves) < resolved_size:
            move_elements.append((None, resolved_size - len(resolved_moves)))

        resolved = Layout(move_elements, 'vertical')
        resolved = Layout([(None, 1), (resolved, 5), (None, 1)], 'horizontal')

        middle_column = Layout([(None, 4), (unresolved, stack_size),
                                (None, 2), (resolved, resolved_size),
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
