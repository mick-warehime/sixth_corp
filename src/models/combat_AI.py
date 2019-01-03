import random
from itertools import product
from typing import Sequence

from models.abilities_base import Ability
from models.states import Stateful


class Move(object):
    def __init__(self, ability: Ability, user: Stateful,
                 target: Stateful) -> None:
        self.ability = ability
        self._user = user
        self.target = target

    def use(self) -> None:
        self.ability.use(self._user, self.target)

    def describe(self) -> str:
        return self.ability.describe_use(self._user, self.target)


def valid_moves(user: Stateful,
                targets: Sequence[Stateful]) -> Sequence[Move]:
    return [Move(a, user, t) for a, t in product(user.abilities(), targets)
            if a.can_use(user, t)]


def random_move(user: Stateful, targets: Sequence[Stateful]) -> Move:
    return random.choice(valid_moves(user, targets))