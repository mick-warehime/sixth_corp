import pytest

from characters.character_examples import CharacterTypes
from characters.character_impl import build_character
from characters.effects import (AcquireMod, ChangeLocation, IncrementAttribute,
                                RestartGame)
from models.characters.mods_base import GenericMod
from characters.player import get_player, reset_player
from models.characters.states import Attributes
from world.locations import LoadingLocation, MarsLocation
from world.world import get_location


@pytest.fixture(scope='function')
def player():
    return get_player()


def teardown_function(function):
    reset_player()


def test_restart_game(player):
    player.status.increment_attribute(Attributes.HEALTH, -1)
    old_health = player.status.get_attribute(Attributes.HEALTH)
    RestartGame().execute()
    assert old_health is not get_player().status.get_attribute(Attributes.HEALTH)


def test_increment_player_attribute(player):
    health = player.status.get_attribute(Attributes.HEALTH)
    delta = -2
    IncrementAttribute(player, Attributes.HEALTH, delta).execute()
    assert player.status.get_attribute(Attributes.HEALTH) == health + delta


def test_increment_attribute():
    char = build_character(CharacterTypes.DRONE.data)
    health = char.status.get_attribute(Attributes.HEALTH)
    delta = -3
    IncrementAttribute(char, Attributes.HEALTH, delta).execute()
    assert char.status.get_attribute(Attributes.HEALTH) == health + delta


def test_acquire_mod(player):
    mod = GenericMod()
    assert mod not in player.inventory.all_mods()
    AcquireMod(mod).execute()
    assert mod in player.inventory.all_mods()


def test_change_location(player):
    location = get_location()
    assert isinstance(location, LoadingLocation)

    ChangeLocation(MarsLocation()).execute()

    new_location = get_location()
    assert isinstance(new_location, MarsLocation)
