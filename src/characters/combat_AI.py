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

    def use(self) -> None:
        self.ability.use(self._user, self.target)

    def describe(self) -> str:
        return self.ability.describe_use(self._user, self.target)


def valid_moves(user: Character,
                targets: Sequence[Stateful]) -> Sequence[Move]:
    return [m for m in all_moves(user, targets) if m.ability.can_use(user, m.target)]


def all_moves(user: Character, targets: Sequence[Stateful]) -> Sequence[Move]:
    return [Move(a, user, t) for a, t in product(user.abilities(), targets)]
