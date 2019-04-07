from abc import abstractmethod
from typing import Sequence

from models.characters.states import Stateful
from models.combat.moves_base import Move


class AI(object):
    """AI for selecting enemy moves during combat."""

    @abstractmethod
    def select_move(self) -> Move:
        """Select the next move for the AI's user."""

    @abstractmethod
    def set_user(self, user: Stateful) -> None:
        """Assign a user (state) to the AI."""

    @abstractmethod
    def set_targets(self, targets: Sequence[Stateful]) -> None:
        """Specify possible targets for moves."""
