import pytest

from models.character_base import Character
from models.effects import RestartGame, IncrementPlayerAttribute, \
    IncrementAttribute, AcquireMod
from models.mod_examples import HelmOfBeingOnFire
from models.player import get_player
from models.states import Attribute

_player = get_player()


@pytest.fixture(scope='function')
def player():
    return _player


def teardown_function(function):
    _player.reset()


def test_restart_world(player):
    RestartGame().execute()
    assert player is not player.player


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
