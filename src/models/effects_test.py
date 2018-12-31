import pytest

from models.character_base import Character
from models.effects import RestartWorld, IncrementPlayerAttribute, \
    IncrementAttribute, AcquireMod
from models.mod_examples import HelmOfBeingOnFire
from models.states import Attribute
from models.world import World

_world = World()


@pytest.fixture(scope='function')
def world():
    return _world


def teardown_function(function):
    _world.reset()


def test_restart_world(world):
    player = world.player
    RestartWorld().execute()
    assert player is not world.player


def test_increment_player_attribute(world):
    health = world.player.get_attribute(Attribute.HEALTH)
    delta = -2
    IncrementPlayerAttribute(Attribute.HEALTH, delta).execute()
    assert world.player.get_attribute(Attribute.HEALTH) == health + delta


def test_increment_attribute(world):
    health = 10
    char = Character(health=health)
    delta = -3
    IncrementAttribute(char, Attribute.HEALTH, delta).execute()
    assert char.get_attribute(Attribute.HEALTH) == health + delta


def test_acquire_mod(world):
    mod = HelmOfBeingOnFire()
    assert mod not in world.player.inventory.all_mods()
    AcquireMod(mod).execute()
    assert mod in world.player.inventory.all_mods()
