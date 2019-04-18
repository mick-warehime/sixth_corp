"""Basic class for player and enemies."""

from functools import partial

from pygame.rect import Rect

from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.chassis import Chassis
from models.characters.inventory import InventoryBase
from models.characters.mods_base import GenericMod
from models.characters.states import Attributes, AttributeType, State, Status
from models.characters.status import BasicStatus
from models.combat.ai_base import AI
from models.combat.ai_impl import build_ai


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
        # CPU bounds.
        self._base_status.set_attribute_bounds(
            Attributes.HEALTH, 0,
            partial(self.get_attribute, Attributes.MAX_HEALTH))
        self._base_status.set_attribute_bounds(
            Attributes.CPU_AVAILABLE, 0,
            partial(self.get_attribute, Attributes.MAX_CPU))

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self._inventory.grants_state(state))

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self._inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)


def build_character(data: CharacterData) -> _CharacterImpl:
    chassis = Chassis.from_data(data.chassis_data)

    ai = build_ai(data.ai_type)
    char = _CharacterImpl(chassis, ai, data.image_path, name=data.name)
    ai.set_user(char)

    for mod_data in data.mods:
        mod = GenericMod(mod_data.states_granted, mod_data.attribute_modifiers,
                         mod_data.subroutines_granted, mod_data.valid_slots)
        assert char.chassis.can_store(mod), 'Mod cannot be picked up.'
        char.chassis.attempt_store(mod)

    health = char.status.get_attribute(Attributes.MAX_HEALTH)
    char.status.increment_attribute(Attributes.HEALTH, health)
    CPU = char.status.get_attribute(Attributes.MAX_CPU)
    char.status.increment_attribute(Attributes.CPU_AVAILABLE, CPU)

    return char
