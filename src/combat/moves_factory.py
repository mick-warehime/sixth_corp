from itertools import product
from typing import Sequence

from characters.abilities_base import Ability
from characters.character_base import Character
from combat.moves_base import Move


class MoveImpl(object):
    def __init__(self, ability: Ability, user: Character,
                 target: Character) -> None:
        self.ability = ability
        self._user = user
        self.target = target

    def execute(self) -> None:
        self.ability.use(self._user, self.target)

    def describe(self) -> str:
        return self.ability.describe_use(self._user, self.target)

    def can_use(self) -> bool:
        return self.ability.can_use(self._user, self.target)

    def __repr__(self) -> str:
        return 'MOVE: {}'.format(self.describe())

    def __str__(self) -> str:
        return self.__repr__()


def valid_moves(user: Character,
                targets: Sequence[Character]) -> Sequence[Move]:
    return [m for m in all_moves(user, targets) if m.can_use()]


def all_moves(user: Character, targets: Sequence[Character]) -> Sequence[Move]:
    return [MoveImpl(a, user, t) for a, t in product(user.abilities(), targets)]
