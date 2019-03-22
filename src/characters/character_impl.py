"""Basic class for player and enemies."""

from functools import partial
from typing import List

from characters.character_base import Character
from characters.character_position import Position
from characters.chassis import Chassis
from characters.inventory import InventoryBase
from characters.states import Attributes, AttributeType, State, Status
from characters.status import BasicStatus
from combat.ai_base import AI
from combat.moves_base import Move


class CharacterImpl(Character):
    """Stateful object with states and attributes affected by mods."""

    def __init__(self, chassis: Chassis, ai: AI, image_path: str,
                 name: str = 'unnamed Character') -> None:
        super().__init__()

        self._inventory: InventoryBase = chassis
        self._status = _CombinedStatus(self._inventory)
        self._image_path = image_path
        self._position: Position = None
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
    def ai(self) -> str:
        return self._ai

    @ai.setter
    def ai(self, ai: 'AI') -> None:
        self._ai = ai

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, pos: Position) -> None:
        self._position = pos

    def select_move(self) -> Move:
        return self._ai.select_move()

    def set_targets(self, targets: List['Character']) -> None:
        self._ai.set_targets(targets)

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
