import pytest

from models.ability_examples import Repair
from models.character_base import Character
from models.conditions import FullHealth
from models.states import Attribute


@pytest.fixture()
def character():
    return Character(10)


def test_repair_ability(character):
    repair = Repair(3)
    assert not repair.can_use(character, character)
    character.increment_attribute(Attribute.HEALTH, -1)
    assert repair.can_use(character, character)
    repair.use(character, character)
    assert FullHealth().check(character)
