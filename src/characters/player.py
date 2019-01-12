"""Implementation of the player class."""
from typing import Dict, Sequence

from characters.ability_examples import FireLaser, Repair
from characters.character_builder import CharacterBuilder
from characters.chassis import Chassis
from characters.mods_base import GenericMod, Mod
from characters.states import Attribute


class _Player(CharacterBuilder):
    def initial_mods(self) -> Sequence[Mod]:
        return [GenericMod(abilities_granted=[FireLaser(2), FireLaser(4), Repair(5)])]

    def chassis(self) -> Chassis:
        pass

    def additional_attributes(self) -> Dict[Attribute, int]:
        return {}

    def max_health(self) -> int:
        return 10

    def image_path(self) -> int:
        return 'src/images/walle.png'

    def character_name(self) -> str:
        return 'Player 1'


_player = None


def get_player() -> _Player:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = _Player().build()
