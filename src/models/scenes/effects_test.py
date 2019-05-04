import pytest

from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.player import get_player, reset_player
from models.characters.states import Attributes
from models.scenes.effects import increment_attribute, restart_game


@pytest.fixture(scope='function')
def player():
    return get_player()


def teardown_function(function):
    reset_player()


def test_restart_game(player):
    player.status.increment_attribute(Attributes.HEALTH, -1)
    old_health = player.status.get_attribute(Attributes.HEALTH)
    restart_game()
    assert old_health is not get_player().status.get_attribute(
        Attributes.HEALTH)


def test_increment_player_attribute(player):
    health = player.status.get_attribute(Attributes.HEALTH)
    delta = -2
    increment_attribute(Attributes.HEALTH, delta, player)
    assert player.status.get_attribute(Attributes.HEALTH) == health + delta


def test_increment_attribute():
    char = build_character(data=CharacterTypes.DRONE.data)
    health = char.status.get_attribute(Attributes.HEALTH)
    delta = -3
    increment_attribute(Attributes.HEALTH, delta, char)
    assert char.status.get_attribute(Attributes.HEALTH) == health + delta
