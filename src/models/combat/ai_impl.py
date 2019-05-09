import random
from enum import Enum
from itertools import product
from random import choice
from typing import Callable, Optional, Sequence, Set

from models.characters.ai_base import AI
from models.characters.character_base import Character
from models.characters.moves_base import Move
from models.characters.states import Attributes
from models.characters.subroutines_base import build_subroutine

SelectionFun = Callable[[Sequence[Move]], Move]

_do_nothing = build_subroutine(num_cpu=0, time_to_resolve=1, description='wait')


class _AIImpl(AI):
    """AI for selecting enemy moves during combat."""

    def __init__(self,
                 select_move_fun: SelectionFun) -> None:
        """Private initializer for concrete AI implementation.

        Use ai_impl.build_ai instead.

        Args:
            select_move_fun: Function that selected the next move in a combat.
                Takes a sequence of (valid) moves as input.
        """
        self._user: Optional[Character] = None
        self._select_move_fun = select_move_fun

    def select_move(self, targets: Sequence[Character]) -> Move:
        assert self._user is not None, 'User not specified.'
        # Valid moves are those which can be used immediately and do not cost
        # more cpu_slots than available.
        slots = self._user.status.get_attribute(Attributes.CPU_AVAILABLE)
        valid_subs = (sub for sub in self._user.chassis.all_subroutines()
                      if sub.cpu_slots() <= slots)

        moves = [Move(sub, self._user, target)
                 for sub, target in product(valid_subs, targets)
                 if sub.can_use(self._user, target)]

        if moves:
            return self._select_move_fun(moves)

        return Move(_do_nothing, self._user, self._user)

    def set_user(self, user: Character) -> None:
        self._user = user


class AIType(Enum):
    Random = 'Random'
    Shuffle = 'Shuffle'
    No_AI = 'No AI'

    def selection_fun(self) -> SelectionFun:
        return _selectors[self]()


def build_ai(ai_type: AIType) -> AI:
    return _AIImpl(ai_type.selection_fun())


def _raise_error(moves: Sequence[Move]) -> Move:
    raise NotImplementedError('No AI has no moves.')


def _random_choice(moves: Sequence[Move]) -> Move:
    if not moves:
        raise ValueError('No moves available.')
    return choice(moves)


class _MoveIterator(object):
    """Runs through all moves once before repeating."""

    def __init__(self) -> None:
        self._used_moves: Set[Move] = set()

    def next_move(self, moves: Sequence[Move]) -> Move:

        unchecked_moves = list(moves)
        random.shuffle(unchecked_moves)
        while unchecked_moves:
            move = unchecked_moves.pop()
            if move not in self._used_moves:
                self._used_moves.add(move)
                return move
        if not self._used_moves:
            raise ValueError('No usable moves.')
        self._used_moves.clear()
        return self.next_move(moves)


_selectors = {AIType.Random: lambda: _random_choice,
              AIType.Shuffle: lambda: _MoveIterator().next_move,
              AIType.No_AI: lambda: _raise_error}
