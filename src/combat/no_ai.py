from combat.ai_impl import AIImpl
from combat.moves_base import Move


class NoAI(AIImpl):

    def select_move(self) -> Move:
        raise NotImplementedError('No AI has no moves.')
