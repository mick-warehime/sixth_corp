"""Basic class for player and enemies."""
from abc import abstractmethod
from typing import List

from characters.character_position import Position
from characters.inventory import InventoryBase
from characters.mods_base import Mod
from characters.states import Stateful


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    @property
    @abstractmethod
    def ai(self) -> 'AI':  # type: ignore
        pass

    @ai.setter
    def ai(self, ai: 'AI') -> None:  # type: ignore
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

    @abstractmethod
    def select_move(self) -> 'Move':  # type: ignore
        pass

    @abstractmethod
    def set_targets(self, targets: List['Character']) -> None:
        pass
