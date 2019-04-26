"""Implementation of the combat stack."""
from typing import List, NamedTuple, Sequence, Tuple

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

    update_stack: Increments time by one unit and adds new moves to the stack.

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

    def update_stack(self, moves: Sequence[Move]) -> None:
        """Update the combat stack according to character actions.

        Before putting moves on the stack, time is advanced by one round and the
        prestack method (if specified in __init__) is called on each move. Moves
        with duration>1 are added at multiple spots in the stack.

        Args:
            moves: Moves to add to the stack after advancing time.

        """
        # Phases:
        # 1. Check resolved_moves for execution.
        # 2. Advance time for moves already on the stack.
        # 3. Add new moves to the stack.

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

        # 3. Process and add new moves to the stack.
        for move in moves:
            duration = move.subroutine.duration()
            time_left = move.subroutine.time_slots()
            for i in range(duration):
                self._add_move(move, time_left + i)

    def _add_move(self, move: Move, time_left: int = None) -> None:
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
