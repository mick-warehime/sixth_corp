"""Implementation of the CombatLogic class."""
from typing import Dict, Iterable, List, Sequence, Tuple

from models.characters.character_base import Character
from models.characters.conditions import is_alive, is_dead
from models.characters.moves_base import Move
from models.characters.states import Attributes
from models.combat.combat_stack import CombatStack


class CombatLogic(object):
    """Class that manages all the business logic involved in combat.

    Specifically, this class handles initialization of characters at the
    beginning of combat, final processing at the end of combat, and ensures
    that moves are implemented correctly during combat. See combat_notes.txt
    for a summary of the combat logic.
    """

    def __init__(self, characters: Sequence[Character]) -> None:
        super().__init__()
        self._characters = tuple(characters)
        self._active_characters = tuple(c for c in self._characters
                                        if is_alive(c))
        self._combat_stack = CombatStack()

        # For moves with multi-turn durations, we need to keep track of how many
        # rounds they have existed so that we can return the CPU to the user
        # exactly when the final execution has occurred. We also apply any
        # possible after-effects at this time.
        self._move_lifetime_registry: Dict[Move, List[int]] = {}
        self._initialize_characters(self._characters)

    @property
    def stack(self) -> CombatStack:
        return self._combat_stack

    def start_round(self, moves: Sequence[Move]) -> None:
        """Update the characters and stack to start the next round."""

        # Advance time for existing moves.
        self._combat_stack.advance_time()

        for move in self._move_lifetime_registry:
            self._move_lifetime_registry[move][0] += 1

        # Process and add new moves to the stack.
        moves = [_make_unique(m) for m in moves]  # See _make_unique docstring

        for move in moves:
            self._register_move(move)

            time_left = move.subroutine.time_to_resolve()
            if move.subroutine.multi_use():
                for i in range(move.subroutine.duration() + 1):
                    self._combat_stack.add_move(move, time_left + i)
            else:
                self._combat_stack.add_move(move, time_left)

    def end_round(self) -> None:
        """Apply finalizing logic at the end of a combat round."""
        # Moves execute when they hit the bottom of the stack (time to resolve
        # goes to zero)
        for move in self._combat_stack.resolved_moves():
            move.execute()

        # Remove finished moves from tracking and apply their after-effects.
        finished_moves = [m for m, (rounds, max_rounds) in
                          self._move_lifetime_registry.items()
                          if rounds == max_rounds or is_dead(m.user)
                          or is_dead(m.target)]

        for move in finished_moves:
            move.subroutine.after_effect(move.user, move.target)
            self._move_lifetime_registry.pop(move)
        self._combat_stack.remove_moves(
            lambda m: is_dead(m.user) or is_dead(m.target))

        self._update_cpu_available(self._characters)

        self._active_characters = tuple(c for c in self._characters
                                        if is_alive(c))

    def all_moves_present(self) -> Tuple[Move, ...]:
        """All moves still being tracked.

        This may include moves in the stack, moves that have just resolved,
        and moves which have resolved but whose duration has not yet expired.
        """

        return tuple(self._move_lifetime_registry)

    def active_characters(self) -> Tuple[Character, ...]:
        return self._active_characters

    def _register_move(self, move: Move) -> None:
        duration = move.subroutine.duration()
        time_to_resolve = move.subroutine.time_to_resolve()
        self._move_lifetime_registry[move] = [0, duration + time_to_resolve]

    def _update_cpu_available(self, characters: Iterable[Character]) -> None:
        cpu_att = Attributes.CPU_AVAILABLE
        # Start with all CPU at max value.
        for char in characters:
            max_cpu = char.status.get_attribute(Attributes.MAX_CPU)
            char.status.increment_attribute(cpu_att, max_cpu)

        # Decrement CPU values for moves in progress.
        for mv in self._move_lifetime_registry:
            mv.user.status.increment_attribute(cpu_att,
                                               -mv.subroutine.cpu_slots())

    def _initialize_characters(self, characters: Iterable[Character]) -> None:
        """Initialize character statuses for combat."""
        for char in characters:
            # SHIELD --> 0
            shield = char.status.get_attribute(Attributes.SHIELD)
            char.status.increment_attribute(Attributes.SHIELD, -shield)

        self._update_cpu_available(characters)


def _make_unique(move: Move) -> Move:
    """Make a move distinct under equality from the input.

    We do this because some moves may appear on the stack more than once with
    the exact same time left. We must have them distinct for proper rendering.
    """
    # subroutine copies are distinct, so replace the move's subroutine.
    move_copy = move._replace(subroutine=move.subroutine.copy())
    assert move != move_copy
    return move_copy
