from itertools import product
from typing import Any, List, NamedTuple, Optional, Sequence, Tuple

from data.constants import FRAMES_PER_SECOND, SCREEN_SIZE, BackgroundImages
from events.events_base import (BasicEvents, EventListener, EventType,
                                SelectCharacterEvent, SelectPlayerMoveEvent)
from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.conditions import is_dead
from models.characters.moves_base import Move
from models.characters.player import get_player
from models.characters.states import Attributes, StatusEffect
from models.characters.subroutines_base import build_subroutine
from models.combat.combat_logic import CombatLogic
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


class MoveInfo(NamedTuple):
    """Data required to represent a move on the screen."""
    move: Move
    time_left: int
    under_char: bool = False  # whether to put this move under the character.

    def time_minus_one(self) -> 'MoveInfo':
        return self._replace(time_left=self.time_left - 1)


class CharacterInfo(NamedTuple):
    """Data required to represent a character on the screen."""
    character: Character
    shields: int
    health: int
    max_health: int
    cpu: int
    max_cpu: int
    active_effects: Tuple[StatusEffect, ...]
    description: str
    image_path: str
    is_dead: bool
    is_selected: bool


class CombatScene(EventListener, Scene):
    """Represents and updates all model data involved during a combat."""

    def __init__(self, enemies: Sequence[Character] = None,
                 win_resolution: Resolution = None,
                 loss_resolution: Resolution = None,
                 background_image: str = None) -> None:
        if enemies is None:
            enemies = (build_character(data=CharacterTypes.DRONE.data),)
        self._enemies: Tuple[Character, ...] = tuple(enemies)
        super().__init__()
        self._player = get_player()

        self._combat_logic = CombatLogic((self._player,) + self._enemies)

        self._win_resolution = win_resolution
        self._loss_resolution = loss_resolution

        self._selected_char: Optional[Character] = None

        self._update_layout()

        # Rect positions
        if background_image is None:
            self._background_image = BackgroundImages.CITY.path
        else:
            self._background_image = background_image

        # Animation data
        self._animation_progress: Optional[float] = None
        self._first_turn = True

    @property
    def animation_progress(self) -> Optional[float]:
        """Progress of a combat scene animation.

        This variable is None if no animation is in progress.
        """
        return self._animation_progress

    @property
    def layout(self) -> Layout:
        return self._layout

    @property
    def background_image(self) -> str:
        return self._background_image

    def available_moves(self) -> List[Move]:
        """All player moves that may be added to the combat stack.

        Returns all moves that may be added to the stack, accounting for the
        current target and available CPU slots.
        """
        if self._selected_char is None:
            return [Move(_wait_one_round, self._player, self._player)]
        return _valid_moves(self._player, [self._selected_char])

    def is_resolved(self) -> bool:
        if all(is_dead(c) for c in self._enemies):
            return True

        return is_dead(self._player)

    def get_resolution(self) -> Resolution:
        assert self.is_resolved()
        if all(is_dead(e) for e in self._enemies):
            assert self._win_resolution is not None, (
                'win resolution unspecified at init.')
            return self._win_resolution
        assert is_dead(self._player)
        assert self._loss_resolution is not None, (
            'loss resolution unspecified at init.')
        return self._loss_resolution

    def notify(self, event: EventType) -> None:
        if isinstance(event, SelectCharacterEvent):
            # Cannot select dead characters
            char = event.character
            if char in self._combat_logic.active_characters() or char is None:
                self._selected_char = char
                self._update_layout()

        # Add new moves to the combat stack and start animation
        if isinstance(event, SelectPlayerMoveEvent):

            moves = [event.move]
            active_chars = self._combat_logic.active_characters()
            moves.extend(e.ai.select_move(active_chars)
                         for e in self._enemies if e in active_chars)
            self._combat_logic.start_round(moves)
            self._selected_char = None
            self._update_layout()

            # If animation enabled, start progress. Otherwise execute moves.
            if ANIMATION and not self._first_turn:
                self._animation_progress = 0.0
            else:
                self._combat_logic.end_round()
                self._update_layout()
            self._first_turn = False

        # Animation in progress
        if event == BasicEvents.TICK and self._animation_progress is not None:
            self._animation_progress += 1.0 / _ticks_per_animation
            # Execute moves once animation is finished
            if self._animation_progress >= 1.0:
                self._animation_progress = None
                self._combat_logic.end_round()
                self._update_layout()

    def __str__(self) -> str:
        return 'CombatScene(enemy = {})'.format(str(self._enemies))

    def _update_layout(self) -> None:
        """Update the screen layout according to moves and characters in scene.
        """

        # The layout is broken up into 3 columns:
        # 1. Player column, which shows player image and stats.
        # 2. Stack column, which shows moves on the stack and those which have
        # just resolved.
        # 3. Enemy column, which shows enemy images and stats.
        # We populate these columns with objects whose attributes (data) are
        # required to render the scene.
        characters = (self._player,) + self._enemies
        all_moves = self._combat_logic.all_moves_present()

        # player side layout
        player = characters[0]

        player_layout = self._character_layout(player, all_moves)
        left_column = Layout([(None, 1), (player_layout, 1), (None, 1)],
                             'vertical')

        # stack layout
        # unresolved moves (and time to resolve)
        moves_times = self._combat_logic.stack.moves_times_remaining()[::-1]
        num_moves = len(moves_times)
        stack_size = 6
        stack_elems: List[Tuple[Any, int]] = [(MoveInfo(*m_t), 1)
                                              for m_t in moves_times]
        # Add a gap rect so that rects are always scaled to the same size by
        # the layout.
        if num_moves <= stack_size:
            stack_elems.append((None, stack_size - num_moves))

        unresolved = Layout(stack_elems, 'vertical')
        unresolved = Layout([(None, 1), (unresolved, 5), (None, 1)],
                            'horizontal')

        # resolved moves
        resolved_size = 4
        resolved_moves = self._combat_logic.stack.resolved_moves()[::-1]
        resolved_elems: List[Tuple[Any, int]] = [(MoveInfo(mv, 0), 1) for mv in
                                                 resolved_moves]
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
            enemy_layout = self._character_layout(enemy, all_moves)

            right_elements.extend([(enemy_layout, 2), (None, 1)])

        right_column = Layout(right_elements, 'vertical')

        self._layout = Layout(
            [(left_column, 2), (middle_column, 3), (right_column, 2)],
            'horizontal', SCREEN_SIZE)

    def _character_layout(self, char: Character,
                          all_moves: Sequence[Move]) -> Layout:

        char_layout = Layout([(None, 1), (self._character_info(char), 2),
                              (None, 1)], 'horizontal')

        move_space = 3
        # Pull out all unique moves by the character
        moves_set = {m for m in all_moves if m.user is char}
        moves = [MoveInfo(m, 0, True) for m in moves_set]

        move_layout = Layout([(m, 1) for m in moves])
        move_layout = Layout([(None, 1), (move_layout, 4), (None, 1)],
                             'horizontal')
        full_elements = [(char_layout, 5), (None, 3),
                         (move_layout, min(move_space, len(moves)))]
        if len(moves) < move_space:
            full_elements.append((None, move_space - len(moves)))

        return Layout(full_elements)

    def _character_info(self, char: Character) -> CharacterInfo:

        def attr_value(attr: Attributes) -> int:
            return char.status.get_attribute(attr)

        return CharacterInfo(char, attr_value(Attributes.SHIELD),
                             attr_value(Attributes.HEALTH),
                             attr_value(Attributes.MAX_HEALTH),
                             attr_value(Attributes.CPU_AVAILABLE),
                             attr_value(Attributes.MAX_CPU),
                             tuple(char.status.active_effects()),
                             char.description(),
                             char.image_path,
                             is_dead(char),
                             char is self._selected_char)
