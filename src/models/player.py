"""Implementation of the player class."""
from models.character_base import Character

STARTING_HEALTH = 10


class _Player(Character):

    def __init__(self):
        super().__init__(STARTING_HEALTH)


_player = None


def get_player() -> _Player:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = _Player()
