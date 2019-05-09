"""Implementation of the combat stack."""
from typing import Callable, List, NamedTuple, Tuple

from models.characters.moves_base import Move


class _TimedMove(NamedTuple):
    move: Move
    time_left: int


class CombatStack(object):
    """Manages the moves in a combat stack.

    Main methods are:

    moves_times_remaining: Moves on the stack that have not yet resolved and
        their time to resolve

    resolved_moves: Moves that have just resolved since the last stack update.

    advance_time: Increments time by one unit.

    """

    def __init__(self) -> None:
        self._stack: List[_TimedMove] = []
        self._just_resolved: Tuple[Move, ...] = ()
        self._resolved_moves_called = True

    def resolved_moves(self) -> Tuple[Move, ...]:
        """Moves that have resolved since the last time update_stack was called.

        This method must be called at least once before each call to
        update_stack.
        """

        self._resolved_moves_called = True

        return self._just_resolved

    def moves_times_remaining(self) -> List[Tuple[Move, int]]:
        """Moves on the stack (and time left) that have not yet resolved.

        Returns a list of tuples of the form (move, time_left) in resolution
        order (first in first resolved).

        """

        return [(tm.move, tm.time_left) for tm in self._stack]

    def advance_time(self) -> None:
        """Advance time by one round.

        Moves whose time left is zero are moved to resolved_moves.

        resolved_moves() must be called at least once before each call of
        advance_time, except after initialization.

        """
        # Phases:
        # 1. Check resolved_moves for execution.
        # 2. Advance time for moves already on the stack.

        # 1. Check that we extracted the previously resolved moves.
        if not self._resolved_moves_called:
            raise ValueError('Must call execute_resolved_moves() before'
                             'successive calls to advance_time.')
        self._resolved_moves_called = False

        # 2. Update time_left for each move and separate resolved moves.
        just_resolved = []
        new_stack: List[_TimedMove] = []

        for timed_move in self._stack:
            assert timed_move.time_left > 0
            if timed_move.time_left == 1:
                just_resolved.append(timed_move.move)
            else:
                new_stack.append(
                    timed_move._replace(time_left=timed_move.time_left - 1))
        self._stack = new_stack
        self._just_resolved = tuple(just_resolved)

    def add_move(self, move: Move, time_left: int) -> None:
        """Add a move to the stack.

        The move is placed on the stack according to its time to resolve. Moves
        that resolve sooner are at the beginning of the stack. If a move already
        exists with the same time to resolve, the current move is placed
        behind it (resolves later).

        Args:
            move: Move to add.
            time_left: Time for the move to resolve.
        """

        assert time_left >= 0

        if time_left == 0:
            self._just_resolved = (move,) + self._just_resolved
            return

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

    def remove_moves(self, condition: Callable[[Move], bool]) -> None:
        """Remove all moves from the stack satisfying a given condition.

        This does not affect resolved moves.
        """
        to_remove = [mt for mt in self._stack if condition(mt.move)]
        for mt in to_remove:
            self._stack.remove(mt)
