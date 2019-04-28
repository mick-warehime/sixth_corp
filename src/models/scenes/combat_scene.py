from itertools import product
from typing import Any, List, NamedTuple, Optional, Sequence, Tuple

from data.constants import FRAMES_PER_SECOND, SCREEN_SIZE, BackgroundImages
from events.events_base import (BasicEvents, EventListener, EventType,
                                SelectCharacterEvent, SelectPlayerMoveEvent)
from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.conditions import IsDead
from models.characters.moves_base import Move
from models.characters.player import get_player
from models.characters.states import Attributes
from models.characters.subroutines_base import build_subroutine
from models.combat.combat_logic import CombatLogic
from models.scenes import scene_examples
from models.scenes.layouts import Layout
from models.scenes.scenes_base import Resolution, Scene

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


class MoveData(NamedTuple):
    """Data required to represent a move on the screen."""
    move: Move
    time_left: int
    under_char: bool = False  # whether to put this move under the character.

    def time_minus_one(self) -> 'MoveData':
        return self._replace(time_left=self.time_left - 1)


class CombatScene(EventListener, Scene):
    """Represents and updates all model data involved during a combat."""

    def __init__(self, enemy: Character = None,
                 win_resolution: Resolution = None,
                 background_image: str = None) -> None:
        if enemy is None:
            enemy = build_character(data=CharacterTypes.DRONE.data)
        self._enemy: Character = enemy
        super().__init__()
        self._player = get_player()

        self._combat_logic = CombatLogic(self.characters())

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
            moves = [event.move, self._enemy.ai.select_move([self._player])]
            self._combat_logic.start_round(moves)
            self._update_layout()
            self._selected_char = None

            # If animation enabled, start progress. Otherwise execute moves.
            if ANIMATION and not self._first_turn:
                self._animation_progress = 0.0
            else:
                self._combat_logic.end_round()
            self._first_turn = False

        # Animation in progress
        if event == BasicEvents.TICK and self.animation_progress is not None:
            self._animation_progress += 1.0 / _ticks_per_animation
            # Execute moves once animation is finished
            if self._animation_progress >= 1.0:
                self._animation_progress = None
                self._combat_logic.end_round()

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self._enemy))

    def _update_layout(self) -> None:
        """Update the screen layout according to moves and characters in scene.
        """

        # The layout is broken up into 3 columns:
        # 1. Player column, which shows player stats.
        # 2. Stack column, which shows moves on the stack and those which have
        # just resolved.
        # 3. Enemy column, which shows enemy stats.
        # We populate these columns with objects whose attributes (data) are
        # required to render the scene.
        characters = self.characters()
        moves_times = self._combat_logic.stack.moves_times_remaining()[::-1]

        # player side layout
        player = characters[0]

        player_layout = _character_layout(player, moves_times)
        left_column = Layout([(None, 1), (player_layout, 1), (None, 1)],
                             'vertical')

        # stack layout
        # unresolved moves (and time to resolve)
        num_moves = len(moves_times)
        stack_size = 6
        stack_elements = [(MoveData(*m_t), 1) for m_t in moves_times]
        # Add a gap rect so that rects are always scaled to the same size by
        # the layout.
        if num_moves <= stack_size:
            stack_elements.append((None, stack_size - num_moves))

        unresolved = Layout(stack_elements, 'vertical')
        unresolved = Layout([(None, 1), (unresolved, 5), (None, 1)],
                            'horizontal')

        # resolved moves
        resolved_size = 4
        resolved_moves = self._combat_logic.stack.resolved_moves()[::-1]
        resolved_elems = [(MoveData(mv, 0), 1) for mv in resolved_moves]
        # Add a gap to ensure consistent rect sizes.
        if len(resolved_moves) < resolved_size:
            resolved_elems.append((None, resolved_size - len(resolved_moves)))

        resolved = Layout(resolved_elems, 'vertical')
        resolved = Layout([(None, 1), (resolved, 5), (None, 1)], 'horizontal')

        middle_column = Layout([(None, 4), (unresolved, stack_size),
                                (None, 2), (resolved, resolved_size),
                                (None, 6)])

        # enemies layout
        assert len(characters) > 1

        right_elements: List[Tuple[Any, int]] = [(None, 1)]
        for enemy in characters[1:]:
            enemy_layout = _character_layout(enemy, moves_times)

            right_elements.extend([(enemy_layout, 2), (None, 1)])

        right_column = Layout(right_elements, 'vertical')

        self._layout = Layout(
            [(left_column, 2), (middle_column, 3), (right_column, 2)],
            'horizontal', SCREEN_SIZE)


def _character_layout(char: Character,
                      moves_with_time: List[Tuple[Move, int]]) -> Layout:
    move_space = 3
    # Pull out all unique moves by the character
    moves_set = {m for m, t in moves_with_time if m.user is char}
    moves = [MoveData(m, 0, True) for m in moves_set]
    char_layout = Layout([(None, 1), (char, 2), (None, 1)], 'horizontal')
    move_layout = Layout([(m, 1) for m in moves])
    move_layout = Layout([(None, 1), (move_layout, 4), (None, 1)],
                         'horizontal')
    full_elements = [(None, 1), (char_layout, 5), (None, 1),
                     (move_layout, min(move_space, len(moves)))]
    if len(moves) < move_space:
        full_elements.append((None, move_space - len(moves)))

    return Layout(full_elements)
