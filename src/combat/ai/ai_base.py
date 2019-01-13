from abc import abstractmethod
from typing import Sequence

from characters.character_base import Character
from combat.moves_base import Move
from combat.moves_factory import all_moves


class AI(object):
    """AI for selecting enemy moves during combat."""

    def __init__(self, user: Character) -> None:
        self._user = user
        self.moves: Sequence[Move] = []
        self._targets: Sequence[Character] = None

    @abstractmethod
    def select_move(self) -> Move:
        pass

    def set_targets(self, targets: Sequence[Character]) -> None:
        self._targets = targets
        self.moves = all_moves(self._user, targets)
