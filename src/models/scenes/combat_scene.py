from functools import reduce
from itertools import product
from typing import List, Optional, Sequence, Tuple

from data.constants import FRAMES_PER_SECOND, SCREEN_SIZE, BackgroundImages
from events.events_base import (BasicEvents, EventListener, EventType,
                                SelectCharacterEvent, SelectPlayerMoveEvent)
from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.conditions import IsDead
from models.characters.player import get_player
from models.characters.states import Attributes
from models.characters.subroutines_base import build_subroutine
from models.combat.combat_stack import CombatStack
from models.combat.moves_base import Move
from models.scenes import scene_examples
from models.scenes.scenes_base import Resolution, Scene
from models.scenes.layouts import Layout

_wait_one_round = build_subroutine(can_use=True, num_cpu=0, time_to_resolve=1,
                                   description='wait one round')

_ANIMATION_TIME_SECONDS = 1.0
_ticks_per_animation = FRAMES_PER_SECOND * _ANIMATION_TIME_SECONDS
ANIMATION = True  # Set to False during integration tests


def _valid_moves(user: Character, targets: Sequence[Character]) -> List[Move]:
    """All valid moves from a user to a sequence of targets, ignoring CPU slots.
    """
    return [Move(sub, user, target)
            for sub, target in
            product(user.chassis.all_subroutines(), targets)
            if sub.can_use(user, target)
            and sub.cpu_slots() <= user.status.get_attribute(
            Attributes.CPU_AVAILABLE)]


def _remove_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()
    assert cpu_slots <= move.user.status.get_attribute(
        Attributes.CPU_AVAILABLE)
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE, -cpu_slots)


def _return_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE, cpu_slots)


class CombatScene(EventListener, Scene):

    def __init__(self, enemy: Character = None,
                 win_resolution: Resolution = None,
                 background_image: str = None) -> None:
        if enemy is None:
            enemy = build_character(CharacterTypes.DRONE.data)
        self._enemy: Character = enemy
        super().__init__()
        self._player = get_player()

        # initialize CPU slots
        for char in self.characters():
            max_cpu = char.status.get_attribute(Attributes.MAX_CPU)
            char.status.increment_attribute(Attributes.CPU_AVAILABLE, max_cpu)

        self._combat_stack = CombatStack(_remove_user_cpu, _return_user_cpu)

        if win_resolution is None:
            win_resolution = scene_examples.ResolutionTypes.RESTART.resolution
        self._win_resolution = win_resolution

        self._selected_char: Character = None

        self._layout: Layout = None
        self._update_layout()

        # Rect positions
        if background_image is None:
            self._background_image = BackgroundImages.CITY.path
        else:
            self._background_image = background_image

        # Animation data
        self._animation_progress: float = None
        self._first_turn = True

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
        """All player moves that may be added to the combat stack.

        Returns all moves that may be added to the stack, accounting for the
        current target and available CPU slots.
        """
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

    def notify(self, event: EventType) -> None:
        if isinstance(event, SelectCharacterEvent):
            self._selected_char = event.character

        # Add new moves to the combat stack and start animation
        if isinstance(event, SelectPlayerMoveEvent):
            enemy_move = self._enemy.ai.select_move([self._player])
            self._combat_stack.update_stack([event.move, enemy_move])
            self._update_layout()
            self._selected_char = None

            # If animation enabled, start progress. Otherwise execute moves.
            if ANIMATION and not self._first_turn:
                self._animation_progress = 0.0
            else:
                self._combat_stack.execute_resolved_moves()
            self._first_turn = False

        # Animation in progress
        if event == BasicEvents.TICK and self.animation_progress is not None:
            self._animation_progress += 1.0 / _ticks_per_animation
            # Execute moves once animation is finished
            if self._animation_progress >= 1.0:
                self._animation_progress = None
                self._combat_stack.execute_resolved_moves()

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self._enemy))

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
        resolved_moves = self.combat_stack.resolved_moves[::-1]
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
            [(left_column, 2), (middle_column, 3), (right_column, 2)],
            'horizontal', SCREEN_SIZE)
