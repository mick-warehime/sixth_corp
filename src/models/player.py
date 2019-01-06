"""Implementation of the player class."""
from models.character_base import Character
from models.ability_examples import FireLaser, Repair

from models.mods_base import GenericMod

STARTING_HEALTH = 10


class _Player(Character):

    def __init__(self):
        super().__init__(STARTING_HEALTH, 'player')

        # We can think of this as the inherent mod of the chassis/ player type.
        # They can be assigned to an immutable "chassis" slot.
        base_abilities = GenericMod(
            abilities_granted=(FireLaser(2), FireLaser(4), Repair(5)))
        self.attempt_pickup(base_abilities)

    def __str__(self):
        return 'player'


_player = None


def get_player() -> _Player:
    global _player
    if _player is None:
        reset_player()
    return _player


def reset_player() -> None:
    global _player
    _player = _Player()
