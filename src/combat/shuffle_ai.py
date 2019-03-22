from random import shuffle
from typing import Iterator, List

from combat.ai_impl import AIImpl
from combat.moves_base import Move


class ShuffleAI(AIImpl):
    """Tries to play all n moves times in random order and reshuffles."""

    def __init__(self) -> None:
        super().__init__()
        self._shuffled_moves: List[Move] = []
        self._last_attemped_play: List[int] = []
        self._move_iterator: Iterator[Move] = None

    def move_iterator(self) -> Iterator[Move]:
        count = 0
        while True:
            shuffle(self.moves)
            used_a_move = False
            for move in self.moves:
                if move.can_use():
                    used_a_move = True
                    count += 1
                    yield move

            if not used_a_move:
                assert False, 'AI Has no valid moves'

    def select_move(self) -> Move:
        if self._move_iterator is None:
            self._move_iterator = self.move_iterator()
        return next(self._move_iterator)
