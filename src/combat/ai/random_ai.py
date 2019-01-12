from random import choice
from combat.ai.ai_base import AI
from combat.moves_base import Move


class RandomAI(AI):

    def select_move(self) -> Move:
        return choice(self._moves)
