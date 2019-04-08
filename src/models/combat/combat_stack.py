"""Implementation of the combat stack."""
from typing import NamedTuple, List, Tuple

from models.combat.moves_base import Move


class _TimedMove(NamedTuple):
    move: Move
    time_left: int


class CombatStack(object):
    """Manages the moves in a combat stack.

    Main methods are:

    moves_remaining: Moves on the stack that have not yet resolved.

    advance_time: Increments time unit by one.

    add_move: Add a move to the stack.

    extract_resolved_moves: Moves that have resolved since the last time
        advance_time was called.



    """

    def __init__(self):
        self._stack: List[_TimedMove] = []
        self._just_resolved: Tuple[Move] = ()
        self._extract_resolved_called = True

    def moves_remaining(self) -> List[List[Move]]:
        """Moves on the stack that have not yet resolved.

        Returns a list of lists. moves_remaining()[k] is the list of moves (in
        resolution order, first in first resolved) that have k time left before
        resolving.
        """
        out: List[List[Move]] = [[]]

        for row in self._stack:
            assert row.time_left > 0
            while row.time_left > len(out) - 1:
                out.append([])
            out[row.time_left].append(row.move)
        return out

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

        # internally the stack is just a list of move, time pairs.
        self._stack.append(_TimedMove(move, time_left))

    def extract_resolved_moves(self) -> Tuple[Move]:
        """Moves that have resolved since the last time advance_time was called.

        This method must be called at least once before each call to
        advance_time.
        """
        self._extract_resolved_called = True
        return self._just_resolved
