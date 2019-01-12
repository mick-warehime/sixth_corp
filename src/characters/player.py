"""Singleton container allowing global access to player."""
from characters.character_base import Character
from characters.player_builder import PlayerBuilder

_player = None


def get_player() -> Character:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = PlayerBuilder().build()
