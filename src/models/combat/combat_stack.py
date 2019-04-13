"""Implementation of the combat stack."""
from typing import NamedTuple, List, Tuple

from models.combat.moves_base import Move


class _TimedMove(NamedTuple):
    move: Move
    time_left: int


# player clicks a character
# player selects a move
# move is added to the stack
# turn completes, time moves
# player can also advance time by 1 if they don't select anything and press
# advance time.
# before time is advanced, the enemies get to choose a move to add as well


class CombatStack(object):
    """Manages the moves in a combat stack.

    Main methods are:

    moves_remaining: Moves on the stack that have not yet resolved.

    advance_time: Increments time unit by one.

    add_move: Add a move to the stack.

    extract_resolved_moves: Extract moves that have resolved since the last time
        advance_time was called.

    """

    def __init__(self) -> None:
        self._stack: List[_TimedMove] = []
        self._just_resolved: Tuple[Move, ...] = ()
        self._extract_resolved_called = True

    def moves_times_remaining(self) -> List[Tuple[Move, int]]:
        """Moves on the stack (and time left) that have not yet resolved.

        Returns a list of tuples of the form (move, time_left) in resolution
        order (first in first resolved).

        """

        return [(tm.move, tm.time_left) for tm in self._stack]

    def advance_time(self) -> None:
        """Advance time by one unit, updating the stack accordingly.

        This method can only be called once after initialization or after
        extract_resolved_moves is called.
        """

        if not self._extract_resolved_called:
            raise ValueError('Must call extract_resolved_moves() before'
                             'successive calls to advance_time.')
        self._extract_resolved_called = False

        # For all moves, decrement time_left by 1. Moves with time_left==1
        # before the decrement are moved to self._just_resolved.

        just_resolved = []
        new_stack: List[_TimedMove] = []

        for timed_move in self._stack:
            time_left = timed_move.time_left
            assert time_left > 0
            if time_left == 1:
                just_resolved.append(timed_move.move)
            else:
                new_stack.append(timed_move._replace(time_left=time_left - 1))
        self._stack = new_stack
        self._just_resolved = tuple(just_resolved)

    def add_move(self, move: Move, time_left: int) -> None:
        """Add a move to the stack.

        The move is placed on the stack according to its time to resolve. Moves
        that resolve sooner are at the beginning of the stack. If a move already
        exists with the same time to resolve, the current move is placed
        behind it (nearer the end).
        """

        index = -1
        for index, _ in enumerate(tm for tm in self._stack
                                  if tm.time_left <= time_left):
            pass

        new_stack = []
        if index >= 0:
            new_stack.extend(self._stack[:(index + 1)])
        new_stack.append(_TimedMove(move, time_left))
        new_stack.extend(self._stack[(index + 1):])

        self._stack = new_stack

    def extract_resolved_moves(self) -> Tuple[Move, ...]:
        """Moves that have resolved since the last time advance_time was called.

        This method must be called at least once before each call to
        advance_time.
        """
        self._extract_resolved_called = True
        return self._just_resolved
