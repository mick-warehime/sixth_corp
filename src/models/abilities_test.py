import pytest

from models.ability_examples import Repair, FireLaser
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


def test_fire_laser(character):
    damage = 3
    fire_laser = FireLaser(damage)
    other_char = Character(5)

    assert not fire_laser.can_use(character, character)
    assert fire_laser.can_use(character, other_char)
    fire_laser.use(character, other_char)
    value = other_char.get_attribute
    assert value(Attribute.HEALTH) == value(Attribute.MAX_HEALTH) - damage


def test_ability_order():
    assert FireLaser(3) < Repair(1)
    assert FireLaser(1) < FireLaser(2)


def test_ability_eq():
    assert FireLaser(1) == FireLaser(1)
    assert FireLaser(1) != 31


def test_ability_hash():
    assert FireLaser(1) in {FireLaser(1)}
