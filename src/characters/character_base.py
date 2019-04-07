"""Basic class for player and enemies."""
from abc import abstractmethod

from characters.inventory import InventoryBase
from models.characters.states import Stateful
from combat.ai_base import AI


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    @property
    @abstractmethod
    def ai(self) -> AI:
        """AI used to determine in-game actions."""

    @property
    @abstractmethod
    def image_path(self) -> str:
        """File path to character image"""

    @property
    @abstractmethod
    def inventory(self) -> InventoryBase:
        """All characters have an inventory."""
