from itertools import product
from typing import Sequence

from models.character_base import Character


class Move(object):
    def __init__(self, ability: 'Ability', user: Character,
                 target: Character) -> None:
        self.ability = ability
        self._user = user
        self._target = target

    def use(self) -> None:
        self.ability.use(self._user, self._target)

    def describe(self) -> str:
        return self.ability.describe_use(self._user, self._target)


def valid_moves(user: Character,
                targets: Sequence[Character]) -> Sequence[Move]:
    return [Move(a, user, t) for a, t in product(user.abilities(), targets)
            if a.can_use(user, t)]
