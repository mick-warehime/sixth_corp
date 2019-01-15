import pytest

from characters.character_examples import CharacterTypes
from characters.character_factory import build_character
from characters.character_impl import CharacterImpl
from characters.effects import (AcquireMod, ChangeLocation, IncrementAttribute,
                                RestartGame)
from characters.mod_examples import HelmOfBeingOnFire
from characters.player import get_player, reset_player
from characters.states import Attribute
from world.locations import LoadingLocation, MarsLocation
from world.world import get_location


@pytest.fixture(scope='function')
def player():
    return get_player()


def teardown_function(function):
    reset_player()


def test_restart_game(player):
    player.increment_attribute(Attribute.HEALTH, -1)
    old_health = player.get_attribute(Attribute.HEALTH)
    RestartGame().execute()
    assert old_health is not get_player().get_attribute(Attribute.HEALTH)


def test_increment_player_attribute(player):
    health = player.get_attribute(Attribute.HEALTH)
    delta = -2
    IncrementAttribute(player, Attribute.HEALTH, delta).execute()
    assert player.get_attribute(Attribute.HEALTH) == health + delta


def test_increment_attribute():
    char = build_character(CharacterTypes.DRONE)
    health = char.get_attribute(Attribute.HEALTH)
    delta = -3
    IncrementAttribute(char, Attribute.HEALTH, delta).execute()
    assert char.get_attribute(Attribute.HEALTH) == health + delta


def test_acquire_mod(player):
    mod = HelmOfBeingOnFire()
    assert mod not in player.inventory.all_mods()
    AcquireMod(mod).execute()
    assert mod in player.inventory.all_mods()


def test_change_location(player):
    location = get_location()
    assert isinstance(location, LoadingLocation)

    ChangeLocation(MarsLocation()).execute()

    new_location = get_location()
    assert isinstance(new_location, MarsLocation)
