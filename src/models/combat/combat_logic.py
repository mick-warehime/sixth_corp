"""Implementation of the CombatLogic class."""
from typing import Dict, Iterable, List, Sequence

from models.characters.character_base import Character
from models.characters.moves_base import Move
from models.characters.states import Attributes
from models.combat.combat_stack import CombatStack


class CombatLogic(object):
    """Class that manages all the business logic involved in combat.

    Specifically, this class handles initialization of characters at the
    beginning of combat, final processing at the end of combat, and ensures
    that moves are implemented correctly during combat. See the Subroutine
    docstring for a description.
    """

    def __init__(self, characters: Sequence[Character]) -> None:
        super().__init__()
        self._characters = tuple(characters)
        _initialize_characters(self._characters)
        self._combat_stack = CombatStack()

    @property
    def stack(self) -> CombatStack:
        return self._combat_stack

    def start_round(self, moves: Sequence[Move]) -> None:
        """Update the characters and stack to start the next round."""

        # Advance time for existing moves.
        self._combat_stack.advance_time()

        for move in _move_lifetime_registry:
            _move_lifetime_registry[move][0] += 1

        # Process and add new moves to the stack.
        moves = [_make_unique(m) for m in moves]  # See _make_unique docstring

        for move in moves:
            _register_move(move)
            _remove_user_cpu(move)

            time_left = move.subroutine.time_slots()
            if not move.subroutine.single_use():
                duration = move.subroutine.duration()
                for i in range(duration):
                    self._combat_stack.add_move(move, time_left + i)
            else:
                self._combat_stack.add_move(move, time_left)

    def end_round(self) -> None:
        """Apply finalizing logic at the end of a combat round."""
        # Moves execute when they hit the bottom of the stack (time to resolve
        # goes to zero)
        for move in self._combat_stack.resolved_moves():
            move.execute()

        # Moves must be tracked after they have been executed, as we must wait
        # the move duration before we apply the moves' subroutine after-effect.
        finished_moves = [m for m, (rounds, max_rounds) in
                          _move_lifetime_registry.items()
                          if rounds == max_rounds]
        for move in finished_moves:
            _return_user_cpu(move)
            move.subroutine.after_effect(move.user, move.target)
            _move_lifetime_registry.pop(move)


# For moves with multi-turn durations, we need to keep track of how many times
# they have been executed so that we can return the CPU to the user exactly
# when the final execution has occurred. We also apply any possible
# after-effects.
_move_lifetime_registry: Dict[Move, List[int]] = {}


def _register_move(move: Move) -> None:
    duration = move.subroutine.duration()
    time_to_resolve = move.subroutine.time_slots()
    _move_lifetime_registry[move] = [0, duration + time_to_resolve - 1]


def _remove_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()

    assert cpu_slots <= move.user.status.get_attribute(Attributes.CPU_AVAILABLE)
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE, -cpu_slots)


def _return_user_cpu(move: Move) -> None:
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE,
                                         move.subroutine.cpu_slots())


def _initialize_characters(characters: Iterable[Character]) -> None:
    """Initialize character statuses for combat."""
    for char in characters:
        # CPU --> MAX_CPU
        max_cpu = char.status.get_attribute(Attributes.MAX_CPU)
        char.status.increment_attribute(Attributes.CPU_AVAILABLE, max_cpu)
        # SHIELD --> 0
        shield = char.status.get_attribute(Attributes.SHIELD)
        char.status.increment_attribute(Attributes.SHIELD, -shield)


def _make_unique(move: Move) -> Move:
    """Make a move distinct under equality from the input.

    We do this because some moves may appear on the stack more than once with
    the exact same time left. We must have them distinct for proper rendering.
    """
    # subroutine copies are distinct, so replace the move's subroutine.
    move_copy = move._replace(subroutine=move.subroutine.copy())
    assert move != move_copy
    return move_copy
