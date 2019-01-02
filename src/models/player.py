"""Implementation of the player class."""
from models.character_base import Character
from models.abilities_base import Ability
from models.ability_examples import FireLaser, Repair
from typing import List

STARTING_HEALTH = 10


class _Player(Character):

    def __init__(self):
        super().__init__(STARTING_HEALTH)

    def __str__(self):
        return 'player'

    def initial_abilities(self) -> List[Ability]:
        return [FireLaser(4), Repair(5)]


_player = None


def get_player() -> _Player:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = _Player()
