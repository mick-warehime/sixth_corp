from itertools import product
from typing import (Any, Dict, Iterable, List, NamedTuple, Optional, Sequence,
                    Tuple)

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


# For moves with multi-turn durations, we need to keep track of how many times
# they have been executed so that we can return the CPU to the user exactly
# when the final execution has occurred.
_move_registry: Dict[Move, List[int]] = {}


def _remove_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()
    duration = move.subroutine.duration()
    _move_registry[move] = [0, duration]

    assert cpu_slots <= move.user.status.get_attribute(
        Attributes.CPU_AVAILABLE)
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE, -cpu_slots)


def _return_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()
    _move_registry[move][0] += 1
    if _move_registry[move][0] == _move_registry[move][1]:
        move.user.status.increment_attribute(Attributes.CPU_AVAILABLE,
                                             cpu_slots)


class CombatMoveData(NamedTuple):
    """Data required to represent a move on the screen."""
    move: Move
    time_left: int
    under_char: bool  # whether to put this move under the character.


def _make_unique(move: Move) -> Move:
    """Make a move distinct under equality from the input.

    We do this because some moves may appear on the stack more than once with
    the exact same time left. We must have them distinct for proper rendering.
    """
    # subroutine copies are distinct, so replace the move's subroutine.
    move_copy = move._replace(subroutine=move.subroutine.copy())
    assert move != move_copy
    return move_copy


def _initialize_characters(characters: Iterable[Character]) -> None:
    """Initialize character statuses for combat."""
    for char in characters:
        # CPU -> MAX_CPU
        max_cpu = char.status.get_attribute(Attributes.MAX_CPU)
        char.status.increment_attribute(Attributes.CPU_AVAILABLE, max_cpu)
        # SHIELD -> 0
        shield = char.status.get_attribute(Attributes.SHIELD)
        char.status.increment_attribute(Attributes.SHIELD, -shield)


class CombatScene(EventListener, Scene):
    """Represents and updates all model data involved during a combat."""

    def __init__(self, enemy: Character = None,
                 win_resolution: Resolution = None,
                 background_image: str = None) -> None:
        if enemy is None:
            enemy = build_character(CharacterTypes.DRONE.data)
        self._enemy: Character = enemy
        super().__init__()
        self._player = get_player()

        # initialize CPU slots
        characters = self.characters()
        _initialize_characters(characters)

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
            moves = [_make_unique(event.move), _make_unique(enemy_move)]
            self._combat_stack.update_stack(moves)
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
        moves_times = self.combat_stack.moves_times_remaining()[::-1]

        # player side layout
        player = characters[0]

        player_layout = _character_layout(player, moves_times)
        left_column = Layout([(None, 1), (player_layout, 1), (None, 1)],
                             'vertical')

        # stack layout
        # unresolved moves (and time to resolve)
        num_moves = len(moves_times)
        stack_size = 6
        move_time_elements = [(m_t, 1) for m_t in moves_times]
        # Add a gap rect so that rects are always scaled to the same size by
        # the layout.
        if num_moves <= stack_size:
            move_time_elements.append((None, stack_size - num_moves))

        unresolved = Layout(move_time_elements, 'vertical')
        unresolved = Layout([(None, 1), (unresolved, 5), (None, 1)],
                            'horizontal')

        # resolved moves
        resolved_size = 4
        resolved_moves = self.combat_stack.resolved_moves[::-1]
        move_elements = [(mv, 1) for mv in resolved_moves]
        # Add a gap to ensure consistent rect sizes.
        if len(resolved_moves) < resolved_size:
            move_elements.append((None, resolved_size - len(resolved_moves)))

        resolved = Layout(move_elements, 'vertical')
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
    moves = [CombatMoveData(m, 0, True) for m in moves_set]
    char_layout = Layout([(None, 1), (char, 2), (None, 1)], 'horizontal')
    move_layout = Layout([(m, 1) for m in moves])
    move_layout = Layout([(None, 1), (move_layout, 4), (None, 1)],
                         'horizontal')
    full_elements = [(None, 1), (char_layout, 5), (None, 1),
                     (move_layout, min(move_space, len(moves)))]
    if len(moves) < move_space:
        full_elements.append((None, move_space - len(moves)))

    return Layout(full_elements)
