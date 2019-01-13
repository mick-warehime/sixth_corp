from abc import abstractmethod
from typing import Sequence

from characters.states import Stateful
from combat.moves_base import Move, all_moves


class AI(object):
    """AI for selecting enemy moves during combat."""

    def __init__(self, user: Stateful) -> None:
        self._user = user
        self.moves: Sequence[Move] = []
        self._targets: Sequence[Stateful] = None

    @abstractmethod
    def select_move(self) -> Move:
        pass

    def set_targets(self, targets: Sequence[Stateful]) -> None:
        self._targets = targets
        self.moves = all_moves(self._user, targets)
