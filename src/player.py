"""Implementation of player class."""
from states import Stateful, Attribute


class Player(Stateful):

    def __init__(self):
        super().__init__()
        self.set_attribute(Attribute.MAX_HEALTH, 10)
        self.set_attribute(Attribute.HEALTH, 10)
