"""Singleton container allowing global access to player."""
from models.characters.character_base import Character
from characters.character_examples import CharacterTypes
from characters.character_factory import build_character

_player = None


def get_player() -> Character:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = build_character(CharacterTypes.HUMAN_PLAYER.data)
