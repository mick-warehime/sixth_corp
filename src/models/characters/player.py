"""Singleton container allowing global access to player."""
from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.states import State

_player = None


def get_player() -> Character:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = build_character(data=CharacterTypes.HUMAN_PLAYER.data)

    # This identifies the character as the player character, which is used in
    # determining teams.
    _player.status.set_state(State.IS_PLAYER, True)
