"""Basic class for player and enemies."""
from models.inventory import BasicInventory
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
        self.inventory = BasicInventory()

    def has_state(self, state: State) -> bool:
        return (self._base_status.has_state(state)
                or self.inventory.grants_state(state))

    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        self._base_status.increment_attribute(attribute, delta)

    def get_attribute(self, attribute: AttributeType) -> int:
        modifier = self.inventory.total_modifier(attribute)
        value = self._base_status.get_attribute(attribute) + modifier
        return self._base_status.value_in_bounds(value, attribute)
