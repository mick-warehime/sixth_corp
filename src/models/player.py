"""Implementation of the player class."""
from models.character_base import Character

STARTING_HEALTH = 10


class _Player(Character):

    def __init__(self):
        super().__init__(STARTING_HEALTH)

    def reset(self):
        self.__init__()


_player = None


def get_player() -> _Player:
    global _player
    if _player is None:
        _player = _Player()
    return _player
