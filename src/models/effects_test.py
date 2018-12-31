from models.character_base import Character
from models.effects import RestartWorld, IncrementAttribute, AcquireMod
from models.mod_examples import HelmOfBeingOnFire
from models.player import Player
from models.states import Attribute
from models.world import World


def test_restart_world():
    world = World()
    player = world.player
    RestartWorld().execute(world)
    assert player is not world.player


def test_increment_player_attribute():
    world = World()
    health = world.player.get_attribute(Attribute.HEALTH)
    delta = -2
    IncrementAttribute(Player(), Attribute.HEALTH, delta).execute(world)
    assert world.player.get_attribute(Attribute.HEALTH) == health + delta


def test_increment_attribute():
    world = World()
    health = 10
    char = Character(health=health)
    delta = -3
    IncrementAttribute(char, Attribute.HEALTH, delta).execute(world)
    assert char.get_attribute(Attribute.HEALTH) == health + delta


def test_acquire_mod():
    world = World()
    mod = HelmOfBeingOnFire()
    assert mod not in world.player.inventory.all_mods()
    AcquireMod(mod).execute(world)
    assert mod in world.player.inventory.all_mods()
