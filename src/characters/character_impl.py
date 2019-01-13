"""Basic class for player and enemies."""
import logging
from typing import List, Sequence

from characters.abilities_base import Ability
from characters.character_base import Character
from characters.character_position import Position
from characters.inventory import BasicInventory, InventoryBase
from characters.mods_base import Mod
from characters.states import Attribute, AttributeType, BasicStatus, State
from combat.ai.ai_base import AI
from combat.moves_base import Move


class CharacterImpl(Character):
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
        self._image_path = image_path
        self._position = Position()
        self._ai: AI = None

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
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, pos: Position) -> None:
        self._position = pos

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

    def select_move(self) -> Move:
        return self._ai.select_move()

    def set_targets(self, targets: List['Character']) -> None:
        self._ai.set_targets(targets)

    def __repr__(self) -> str:
        return self._name
