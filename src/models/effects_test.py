from models.character_base import Character
from models.effects import RestartWorld, IncrementAttribute, AcquireMod
from models.mod_examples import HelmOfBeingOnFire
from models.player import Player
from models.states import Attribute


def test_restart_world():
    player = Player()
    RestartWorld().execute()
    assert player is not Player()


def test_increment_player_attribute():
    health = Player().get_attribute(Attribute.HEALTH)
    delta = -2
    IncrementAttribute(Player(), Attribute.HEALTH, delta).execute()
    assert Player().get_attribute(Attribute.HEALTH) == health + delta


def test_increment_attribute():
    health = 10
    char = Character(health=health)
    delta = -3
    IncrementAttribute(char, Attribute.HEALTH, delta).execute()
    assert char.get_attribute(Attribute.HEALTH) == health + delta


def test_acquire_mod():
    mod = HelmOfBeingOnFire()
    assert mod not in Player().all_mods()
    AcquireMod(Player(), mod).execute()
    assert mod in Player().all_mods()
