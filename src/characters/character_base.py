"""Basic class for player and enemies."""
import logging
from typing import Sequence

from characters.abilities_base import Ability
from characters.inventory import BasicInventory, InventoryBase
from characters.mods_base import Mod
from characters.states import (Attribute, AttributeType, BasicStatus, State,
                               Stateful)


class Position(object):

    def __init__(self, x: int =0, y: int =0, w: int =0, h: int =0) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    def __init__(self, health: int, image_path: str = None, name: str = None) -> None:
        super().__init__()
        status = BasicStatus()
        status.set_attribute(Attribute.MAX_HEALTH, health)
        status.set_attribute(Attribute.HEALTH, health)
        status.set_attribute_bounds(Attribute.HEALTH, 0, Attribute.MAX_HEALTH)
        self._name = name if name is not None else 'unnamed Character'

        self._base_status = status
        self._inventory: InventoryBase = BasicInventory()
        self.image_path = image_path
        self.position = Position()

    def attempt_pickup(self, mod: Mod) -> None:
        mod_type = mod.__class__.__name__
        if self._inventory.can_store(mod):
            logging.debug('{} picking up {}'.format(self, mod_type))
            self._inventory.store(mod)
        else:
            logging.debug(
                '{} attempted to pickup {} but was unable.'.format(self,
                                                                   mod_type))

    def abilities(self) -> Sequence[Ability]:
        return self._inventory.all_abilities()

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self._inventory.grants_state(state))

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self._inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)

    def description(self) -> str:
        return self._name

    def set_position(self, x: int, y: int, w: int, h: int) -> None:
        self.position = Position(x, y, w, h)
