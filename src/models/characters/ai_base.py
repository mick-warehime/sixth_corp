from abc import abstractmethod
from typing import TYPE_CHECKING, Sequence

from models.characters.moves_base import Move

if TYPE_CHECKING:
    from models.characters.character_base import Character  # noqa: F401


class AI(object):
    """AI for selecting enemy moves during combat."""

    @abstractmethod
    def select_move(self, targets: Sequence['Character']) -> Move:
        """Select the next move for the AI's user.
        """

    @abstractmethod
    def set_user(self, user: 'Character') -> None:
        """Assign a user (state) to the AI."""
