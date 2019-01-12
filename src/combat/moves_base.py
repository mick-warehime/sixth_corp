import logging
from itertools import product
from typing import Sequence

from characters.abilities_base import Ability
from characters.character_base import Character
from characters.states import Stateful


class Move(object):
    def __init__(self, ability: Ability, user: Stateful,
                 target: Stateful) -> None:
        self.ability = ability
        self._user = user
        self.target = target

    def execute(self) -> None:
        logging.debug('MOVE: {}'.format(self.describe()))
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
                targets: Sequence[Stateful]) -> Sequence[Move]:
    return [m for m in all_moves(user, targets) if m.can_use()]


def all_moves(user: Character, targets: Sequence[Stateful]) -> Sequence[Move]:
    return [Move(a, user, t) for a, t in product(user.abilities(), targets)]
