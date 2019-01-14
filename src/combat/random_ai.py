from random import choice

from combat.ai_impl import AIImpl
from combat.moves_base import Move


class RandomAI(AIImpl):

    def select_move(self) -> Move:
        moves = [m for m in self.moves if m.can_use()]
        assert len(moves) > 0, 'Random AI has no valid moves'
        return choice(moves)
