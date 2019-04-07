"""Basic class for player and enemies."""

from functools import partial

from pygame.rect import Rect

from characters.character_base import Character
from characters.chassis import Chassis
from characters.inventory import InventoryBase
from models.characters.states import Attributes, AttributeType, State, Status
from characters.status import BasicStatus
from combat.ai_base import AI


class CharacterImpl(Character):
    """Stateful object with states and attributes affected by mods."""

    def __init__(self, chassis: Chassis, ai: AI, image_path: str,
                 name: str = 'unnamed Character') -> None:
        super().__init__()

        self._inventory: InventoryBase = chassis
        self._status = _CombinedStatus(self._inventory)
        self._image_path = image_path
        self._rect: Rect = None
        self._ai: AI = ai
        self._name = name

    @property
    def status(self) -> Status:
        return self._status

    @property
    def inventory(self) -> InventoryBase:
        return self._inventory

    @property
    def image_path(self) -> str:
        return self._image_path

    @property
    def ai(self) -> AI:
        return self._ai

    def __repr__(self) -> str:
        return self.description()

    def description(self) -> str:
        return self._name


class _CombinedStatus(Status):
    """In-game state deriving from a BasisStatus and an Inventory.

    The mods in the inventory augment the states and attributes of the basic
    status.
    """

    def __init__(self, inventory: InventoryBase) -> None:
        self._base_status = BasicStatus()
        self._inventory = inventory

        self._base_status.set_attribute_bounds(
            Attributes.HEALTH, 0,
            partial(self.get_attribute, Attributes.MAX_HEALTH))

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self._inventory.grants_state(state))

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self._inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)
