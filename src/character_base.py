"""Basic class for player and enemies."""
from states import Stateful, Attribute


class Character(Stateful):

    def __init__(self, health: int) -> None:
        super().__init__()
        self.set_attribute(Attribute.MAX_HEALTH, health)
        self.set_attribute(Attribute.HEALTH, health)
        self.set_attribute_bounds(Attribute.HEALTH, 0, Attribute.MAX_HEALTH)
