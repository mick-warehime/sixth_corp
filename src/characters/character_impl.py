"""Basic class for player and enemies."""
import logging
from functools import partial
from typing import List, Sequence

from characters.abilities_base import Ability
from characters.character_base import Character
from characters.character_position import Position
from characters.chassis import Chassis
from characters.chassis_examples import ChassisTypes
from characters.chassis_factory import build_chassis
from characters.inventory import InventoryBase
from characters.mods_base import Mod
from characters.states import Attribute, AttributeType, BasicStatus, State
from combat.ai_base import AI
from combat.moves_base import Move


class CharacterImpl(Character):
    """Stateful object with states and attributes affected by mods."""

    def __init__(self, chassis: Chassis = None, image_path: str = None,
                 name: str = 'unnamed Character') -> None:
        super().__init__()
        if chassis is None:
            chassis = build_chassis(ChassisTypes.WALLE.data)
        self._name = name
        self.inventory: InventoryBase = chassis
        self._base_status = BasicStatus()
        self._image_path = image_path
        self._position: Position = None
        self._ai: AI = None

        self._base_status.set_attribute_bounds(
            Attribute.HEALTH, 0,
            partial(self.get_attribute, Attribute.MAX_HEALTH))

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

    def attempt_pickup(self, mod: Mod) -> None:
        mod_type = mod.__class__.__name__
        if self.inventory.can_store(mod):
            logging.debug('{} picking up {}'.format(self, mod_type))
            self.inventory.store(mod)
        else:
            logging.debug(
                '{} attempted to pickup {} but was unable.'.format(self,
                                                                   mod_type))

    def abilities(self) -> Sequence[Ability]:
        return self.inventory.all_abilities()

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self.inventory.grants_state(state))

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self.inventory.total_modifier(attribute)
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
