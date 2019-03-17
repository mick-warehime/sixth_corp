from itertools import product
from typing import Sequence

from characters.character_base import Character
from characters.subroutines_base import Subroutine
from combat.moves_base import Move


class MoveImpl(object):
    def __init__(self, subroutine: Subroutine, user: Character,
                 target: Character) -> None:
        self.subroutine = subroutine
        self.user = user
        self.target = target

    def execute(self) -> None:
        self.subroutine.use(self.user, self.target)

    def describe(self) -> str:
        return self.subroutine.describe_use(self.user, self.target)

    def can_use(self) -> bool:
        return self.subroutine.can_use(self.user, self.target)

    def __repr__(self) -> str:
        return 'MOVE: {}'.format(self.describe())

    def __str__(self) -> str:
        return self.__repr__()


def build_move(subroutine: Subroutine, user: Character,
               target: Character) -> Move:
    return MoveImpl(subroutine, user, target)


def valid_moves(user: Character,
                targets: Sequence[Character]) -> Sequence[Move]:
    return [m for m in all_moves(user, targets) if m.can_use()]


def all_moves(user: Character, targets: Sequence[Character]) -> Sequence[Move]:
    return [MoveImpl(a, user, t) for a, t in
            product(user.inventory.all_subroutines(), targets)]
