from random import shuffle
from typing import List, Sequence

from characters.character_base import Character
from combat.ai.ai_base import AI
from combat.moves_base import Move


class ShuffleAI(AI):
    """Play all n moves {shuffle_size} times in random order and reshuffles."""

    def __init__(self, user: Character, shuffle_size=1) -> None:
        super().__init__(user)
        self._shuffled_moves: List[Move] = []
        self._shuffle_size = shuffle_size

    def select_move(self) -> Move:
        if len(self._shuffled_moves) == 0:
            self._shuffled_moves = self.shuffle()

        return self._shuffled_moves.pop(0)

    def shuffle(self) -> Sequence[Move]:
        moves = self.moves * self._shuffle_size
        shuffle(moves)
        return moves
