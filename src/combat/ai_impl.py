
from typing import Callable, Sequence

from characters.character_base import Character
from characters.states import Stateful
from combat.ai_base import AI
from combat.moves_base import Move
from combat.moves_factory import all_moves

SelectionFun = Callable[[Sequence[Move]], Move]


class AIImpl(AI):
    """AI for selecting enemy moves during combat."""

    def __init__(self,
                 select_move_fun: SelectionFun) -> None:
        self._user = None
        self.moves: Sequence[Move] = []
        self._targets: Sequence[Character] = None
        self._select_move_fun = select_move_fun

    def select_move(self) -> Move:
        return self._select_move_fun(self.moves)

    def set_user(self, user: Stateful) -> None:
        self._user = user

    def set_targets(self, targets: Sequence[Character]) -> None:
        assert self._user is not None, 'Must set user first.'
        self._targets = targets

        self.moves = all_moves(self._user, targets)
