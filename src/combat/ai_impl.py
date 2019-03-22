from abc import abstractmethod
from typing import Sequence

from characters.character_base import Character
from characters.states import Stateful
from combat.ai_base import AI
from combat.moves_base import Move
from combat.moves_factory import all_moves


class AIImpl(AI):
    """AI for selecting enemy moves during combat."""

    def __init__(self) -> None:
        self._user = None
        self.moves: Sequence[Move] = []
        self._targets: Sequence[Character] = None

    @abstractmethod
    def select_move(self) -> Move:
        pass

    def set_user(self, user: Stateful)->None:
        self._user = user

    def set_targets(self, targets: Sequence[Character]) -> None:
        assert self._user is not None, 'Must set user first.'
        self._targets = targets

        self.moves = all_moves(self._user, targets)
