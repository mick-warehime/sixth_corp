from typing import Sequence, Any
from abc import abstractmethod
from combat.moves_base import Move


class AI(object):
    """Helper class for selecting enemy moves during combat."""

    def __init__(self, moves: Sequence[Move]) -> None:
        self._moves = moves

    @abstractmethod
    def select_move(self) -> Move:
        pass
