"""Basic class for player and enemies."""

from functools import partial
from typing import Callable, Iterable, Sequence

from pygame.rect import Rect

from models.characters.ai_base import AI
from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.chassis import Chassis
from models.characters.chassis_examples import ChassisTypes
from models.characters.inventory import InventoryBase
from models.characters.mods_base import Mod, build_mod
from models.characters.states import (Attributes, AttributeType, State, Status,
                                      StatusEffect)
from models.characters.status import BasicStatus
from models.combat.ai_impl import AIType, build_ai


class _CharacterImpl(Character):
    """Stateful object with states and attributes affected by mods."""

    def __init__(self, chassis: Chassis, ai: AI, image_path: str,
                 name: str = 'unnamed Character') -> None:
        super().__init__()

        self._chassis: Chassis = chassis
        self._status = _CombinedStatus(self._chassis)
        self._image_path = image_path
        self._rect: Rect = None
        self._ai: AI = ai
        self._name = name

    @property
    def status(self) -> Status:
        return self._status

    @property
    def chassis(self) -> Chassis:
        return self._chassis

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

        # We use attribute getters for the composite object to set health and
        # CPU bounds. The base status is used to compute bounds.
        self._base_status.set_attribute_bounds(
            Attributes.HEALTH, None,
            partial(self.get_attribute, Attributes.MAX_HEALTH))
        self._base_status.set_attribute_bounds(
            Attributes.CPU_AVAILABLE, None,
            partial(self.get_attribute, Attributes.MAX_CPU))
        self._base_status.set_attribute_bounds(Attributes.SHIELD, 0, 1000000)

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self._inventory.grants_state(state))

    def set_state(self, state: State, value: bool) -> None:
        self._base_status.set_state(state, value)

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self._inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)

    def add_status_effect(self, effect: StatusEffect) -> None:
        self._base_status.add_status_effect(effect)

    def remove_status_effect(self, effect: StatusEffect) -> None:
        self._base_status.remove_status_effect(effect)

    def active_effects(self, check: Callable[[StatusEffect], bool] = None
                       ) -> Sequence[StatusEffect]:
        return self._base_status.active_effects(check)


def build_character(chassis: Chassis = None, ai_type: AIType = AIType.No_AI,
                    mods: Iterable[Mod] = (),
                    name: str = 'unnamed Character',
                    image_path: str = 'src/data/images/drone.png',
                    data: CharacterData = None) -> _CharacterImpl:
    """Factory function for Characters.

    Args:
        chassis: Character chassis. Default is the Drone chassis defined by
           ChassisTypes.DRONE.
        ai_type: AI assigned to the character. Default is NO_AI (human).
        mods: Mods that the character initially picks up. These are picked up
           in order. If a mod cannot be picked up an error is raised.
        name: Character name.
        image_path: Path to character image. Default is drone image.
        data: (Optional) A CharacterData object containing all desired
            properties. If this is passed, other arguments are ignored.

    Returns:
        A Character with the specified properties.
    """
    if data is not None:
        chassis = Chassis.from_data(data.chassis_data)
        mods = (build_mod(data=m_data) for m_data in data.mods)
        return build_character(chassis, data.ai_type, mods, data.name,
                               data.image_path)

    ai = build_ai(ai_type)
    if chassis is None:
        chassis = Chassis.from_data(ChassisTypes.DRONE.data)
    char = _CharacterImpl(chassis, ai, image_path, name=name)
    ai.set_user(char)

    for mod in mods:
        assert char.chassis.can_store(mod), 'Mod cannot be picked up.'
        char.chassis.attempt_store(mod)

    # Initialize starting health and CPU
    health = char.status.get_attribute(Attributes.MAX_HEALTH)
    char.status.increment_attribute(Attributes.HEALTH, health)
    cpu = char.status.get_attribute(Attributes.MAX_CPU)
    char.status.increment_attribute(Attributes.CPU_AVAILABLE, cpu)

    return char
