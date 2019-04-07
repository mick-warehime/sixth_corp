import random
from enum import Enum
from itertools import product
from random import choice
from typing import Callable, Sequence

from models.characters.character_base import Character
from models.characters.states import Stateful
from models.combat.ai_base import AI
from models.combat.moves_base import Move

SelectionFun = Callable[[Sequence[Move]], Move]


class _AIImpl(AI):
    """AI for selecting enemy moves during combat."""

    def __init__(self,
                 select_move_fun: SelectionFun) -> None:
        """Private initializer for concrete AI implementation.

        Use ai_impl.build_ai instead.

        Args:
            select_move_fun: Function that selected the next move in a combat.
        """
        self._user = None
        self.moves: Sequence[Move] = []
        self._targets: Sequence[Character] = None
        self._select_move_fun = select_move_fun

    def select_move(self) -> Move:
        return self._select_move_fun(self.moves)

    def set_user(self, user: Stateful) -> None:
        self._user = user

    def set_targets(self, targets: Sequence[Character]) -> None:
        assert self._user is not None, 'Must set user first.'
        self._targets = targets

        self.moves = [Move(a, self._user, t) for a, t in
                      product(self._user.inventory.all_subroutines(), targets)]


class AIType(Enum):
    Random = 'Random'
    Shuffle = 'Shuffle'
    Human = 'Human'

    def selection_fun(self) -> SelectionFun:
        return _selectors[self]()


def build_ai(ai_type: AIType) -> AI:
    return _AIImpl(ai_type.selection_fun())


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
