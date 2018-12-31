import pytest

from models.character_base import Character
from models.effects import RestartGame, IncrementPlayerAttribute, \
    IncrementAttribute, AcquireMod
from models.mod_examples import HelmOfBeingOnFire
from models.player import get_player, reset_player
from models.states import Attribute


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
    IncrementPlayerAttribute(Attribute.HEALTH, delta).execute()
    assert player.get_attribute(Attribute.HEALTH) == health + delta


def test_increment_attribute():
    health = 10
    char = Character(health=health)
    delta = -3
    IncrementAttribute(char, Attribute.HEALTH, delta).execute()
    assert char.get_attribute(Attribute.HEALTH) == health + delta


def test_acquire_mod(player):
    mod = HelmOfBeingOnFire()
    assert mod not in player.inventory.all_mods()
    AcquireMod(mod).execute()
    assert mod in player.inventory.all_mods()
