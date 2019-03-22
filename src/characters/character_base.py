"""Basic class for player and enemies."""
from abc import abstractmethod

from characters.character_position import Position
from characters.inventory import InventoryBase
from characters.states import Stateful
from combat.ai_base import AI


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    @property
    @abstractmethod
    def ai(self) -> AI:
        pass

    @property
    @abstractmethod
    def image_path(self) -> str:
        pass

    @property
    @abstractmethod
    def position(self) -> Position:
        pass

    @position.setter
    def position(self, pos: Position) -> None:
        pass

    @property
    @abstractmethod
    def inventory(self) -> InventoryBase:
        """All characters have an inventory."""
