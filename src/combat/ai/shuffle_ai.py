from random import shuffle
from typing import List, Sequence

from combat.ai.ai_base import AI
from combat.moves_base import Move


class ShuffleAI(AI):
    """Play all n moves {shuffle_size} times in random order and reshuffles."""

    def __init__(self, moves: Sequence[Move], shuffle_size=1) -> None:
        super().__init__(moves)
        self._turn = 0
        self._shuffled_moves: List[Move] = []
        self._shuffle_size = shuffle_size

    def select_move(self) -> Move:
        if len(self._shuffled_moves) == 0:
            self._shuffled_moves = self.shuffle()

        return self._shuffled_moves.pop(0)

    def shuffle(self) -> Sequence[Move]:
        moves = self._moves * self._shuffle_size
        shuffle(moves)
        return moves
