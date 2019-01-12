from random import choice

from combat.ai.ai_base import AI
from combat.moves_base import Move


class RandomAI(AI):

    def select_move(self) -> Move:
        moves = [m for m in self._all_moves if m.can_use()]
        return choice(moves)
