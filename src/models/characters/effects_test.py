import pytest

from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.effects import (AcquireMod, IncrementAttribute,
                                       RestartGame)
from models.characters.mods_base import GenericMod
from models.characters.player import get_player, reset_player
from models.characters.states import Attributes


@pytest.fixture(scope='function')
def player():
    return get_player()


def teardown_function(function):
    reset_player()


def test_restart_game(player):
    player.status.increment_attribute(Attributes.HEALTH, -1)
    old_health = player.status.get_attribute(Attributes.HEALTH)
    RestartGame().execute()
    assert old_health is not get_player().status.get_attribute(
        Attributes.HEALTH)


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
    assert mod not in player.chassis.all_mods()
    AcquireMod(mod).execute()
    assert mod in player.chassis.all_mods()
