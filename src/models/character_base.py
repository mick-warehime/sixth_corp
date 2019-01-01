"""Basic class for player and enemies."""
import logging

from models.inventory import BasicInventory, InventoryBase
from models.mods_base import Mod
from models.states import Attribute, AttributeType, Stateful, BasicStatus, State


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    def __init__(self, health: int) -> None:
        super().__init__()
        status = BasicStatus()
        status.set_attribute(Attribute.MAX_HEALTH, health)
        status.set_attribute(Attribute.HEALTH, health)
        status.set_attribute_bounds(Attribute.HEALTH, 0, Attribute.MAX_HEALTH)

        self._base_status = status
        self._inventory: InventoryBase = BasicInventory()

    def attempt_pickup(self, mod: Mod) -> None:
        if self._inventory.can_store(mod):
            logging.debug('{} picking up mod {}'.format(self, mod))
            self._inventory.store(mod)
        else:
            logging.debug(
                '{} attempted to pickup {} but was unable.'.format(self, mod))

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self._inventory.grants_state(state))

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self._inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)
