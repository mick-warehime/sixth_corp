"""Singleton container allowing global access to player."""
from characters.character_base import Character
from characters.character_examples import CharacterTypes

_player = None


def get_player() -> Character:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = CharacterTypes.HUMAN_PLAYER.build()
