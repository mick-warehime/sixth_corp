"""Basic class for player and enemies."""

from abc import abstractmethod
from typing import TYPE_CHECKING

from models.characters.states import Stateful

if TYPE_CHECKING:
    from models.combat.ai_base import AI  # noqa: F401
    from models.characters.inventory import InventoryBase  # noqa: F401


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    @property
    @abstractmethod
    def ai(self) -> 'AI':
        """AI used to determine in-game actions."""

    @property
    @abstractmethod
    def image_path(self) -> str:
        """File path to character image"""

    @property
    @abstractmethod
    def inventory(self) -> 'InventoryBase':
        """All characters have an inventory."""
