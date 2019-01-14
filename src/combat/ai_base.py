from abc import abstractmethod

from combat.moves_base import Move


class AI(object):
    """AI for selecting enemy moves during combat."""

    @abstractmethod
    def select_move(self) -> Move:
        pass
