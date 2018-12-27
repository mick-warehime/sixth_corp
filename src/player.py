"""Implementation of player class."""
from states import Stateful, Attribute


class Player(Stateful):

    def __init__(self) -> None:
        super().__init__()
        self.set_attribute(Attribute.MAX_HEALTH, 15)
        self.set_attribute(Attribute.HEALTH, 10)
        self.set_attribute_bounds(Attribute.HEALTH, 0,
                                  lambda x: x.get_attribute(
                                      Attribute.MAX_HEALTH))
