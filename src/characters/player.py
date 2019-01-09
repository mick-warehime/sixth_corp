"""Implementation of the player class."""
from characters.ability_examples import FireLaser, Repair
from characters.character_base import Character
from characters.mods_base import GenericMod

STARTING_HEALTH = 10

_PLAYER_IMAGE = 'src/images/walle.png'

class _Player(Character):

    def __init__(self) -> None:
        super().__init__(STARTING_HEALTH, image_path=_PLAYER_IMAGE, name='player')

        # We can think of this as the inherent mod of the chassis/ player type.
        # They can be assigned to an immutable "chassis" slot.
        base_abilities = GenericMod(
            abilities_granted=(FireLaser(2), FireLaser(4), Repair(5)))
        self.attempt_pickup(base_abilities)
        self.set_position(200, 700, 150, 150)

    def __str__(self) -> str:
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
