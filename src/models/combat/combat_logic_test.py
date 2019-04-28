import pytest

from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.player import reset_player, get_player
from models.characters.states import Attributes
from models.combat.combat_logic import CombatLogic


@pytest.fixture()
def player_char():
    reset_player()
    return get_player()


@pytest.fixture()
def enemy():
    return build_character(CharacterTypes.DRONE.data)


def test_combat_logic_initializes_CPU(player_char, enemy):
    chars = [player_char, enemy]
    for char in chars:
        cpu = char.status.get_attribute(Attributes.CPU_AVAILABLE)
        char.status.increment_attribute(Attributes.CPU_AVAILABLE, -cpu)

    CombatLogic(chars)

    for char in chars:
        actual = char.status.get_attribute(Attributes.CPU_AVAILABLE)
        expected = char.status.get_attribute(Attributes.MAX_CPU)
        assert actual == expected


