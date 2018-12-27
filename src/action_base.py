"""Basic interface for interacting with Characters."""
from character_base import Character


class Action(object):

    def apply(self, character: Character) -> None:
        raise NotImplementedError
