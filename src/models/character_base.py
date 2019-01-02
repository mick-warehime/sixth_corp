"""Basic class for player and enemies."""
import logging
from typing import Any, List
from models.inventory import BasicInventory, InventoryBase
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
        self._abilities = self.initial_abilities()

    def initial_abilities(self) -> List['Ability']:
        return []

    def attempt_pickup(self, mod: 'Mod') -> None:
        mod_type = mod.__class__.__name__
        if self._inventory.can_store(mod):
            logging.debug('{} picking up {}'.format(self, mod_type))
            self._inventory.store(mod)
        else:
            logging.debug(
                '{} attempted to pickup {} but was unable.'.format(self,
                                                                   mod_type))

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self._inventory.grants_state(state))

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self._inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)

    def get_moves(self, target: 'Character') -> List['Move']:
        moves = []
        for ability in self._abilities:
            for potential_target in [self, target]:
                if ability.can_use(self, potential_target):
                    move = Move(ability, self, potential_target)
                    moves.append(move)
        return moves


class Move(object):
    def __init__(self, ability: 'Ability', user: Character, target: Character) -> None:
        self.ability = ability
        self.user = user
        self.target = target

    def use(self) -> None:
        self.ability.use(self.user, self.target)

    def describe(self) -> str:
        return self.ability.describe_use(self.user, self.target)
