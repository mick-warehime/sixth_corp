import random
from enum import Enum
from random import choice
from typing import Sequence

from combat.ai_base import AI
from combat.ai_impl import AIImpl, SelectionFun
from combat.moves_base import Move


class AIType(Enum):
    Random = 'Random'
    Shuffle = 'Shuffle'
    Human = 'Human'

    def selection_fun(self) -> SelectionFun:
        return _selectors[self]()


def _raise_error(moves: Sequence[Move]) -> Move:
    raise NotImplementedError('No AI has no moves.')


def _random_choice(moves: Sequence[Move]) -> Move:
    usable_moves = [move for move in moves if move.is_usable()]
    if not usable_moves:
        raise ValueError('No moves available.')
    return choice(usable_moves)


class _MoveIterator(object):
    """Runs through all usable moves once before repeating."""

    def __init__(self):
        self._used_moves = set()

    def next_move(self, moves: Sequence[Move]) -> Move:

        unchecked_moves = list(moves)
        random.shuffle(unchecked_moves)
        while unchecked_moves:
            move = unchecked_moves.pop()
            if move.is_usable() and move not in self._used_moves:
                self._used_moves.add(move)
                return move
        if not self._used_moves:
            raise ValueError('No usable moves.')
        self._used_moves.clear()
        return self.next_move(moves)


_selectors = {AIType.Random: lambda: _random_choice,
              AIType.Shuffle: lambda: _MoveIterator().next_move,
              AIType.Human: lambda: _raise_error}


def build_ai(ai_type: AIType) -> AI:
    return AIImpl(ai_type.selection_fun())
