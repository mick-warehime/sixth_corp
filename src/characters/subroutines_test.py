import pytest

from characters.character_examples import CharacterData
from characters.character_factory import build_character
from characters.chassis_examples import ChassisTypes
from characters.conditions import FullHealth
from characters.states import Attribute
from characters.subroutine_examples import FireLaser, Repair


@pytest.fixture()
def character():
    return build_character(CharacterData(ChassisTypes.NO_LEGS.data))


def test_repair_subroutine(character):
    repair = Repair(3)
    assert not repair.can_use(character, character)
    character.increment_attribute(Attribute.HEALTH, -1)
    assert repair.can_use(character, character)
    repair.use(character, character)
    assert FullHealth().check(character)


def test_fire_laser(character):
    damage = 3
    fire_laser = FireLaser(damage)
    other_char = build_character(CharacterData(ChassisTypes.NO_LEGS.data))

    assert not fire_laser.can_use(character, character)
    assert fire_laser.can_use(character, other_char)
    fire_laser.use(character, other_char)
    value = other_char.get_attribute
    assert value(Attribute.HEALTH) == value(Attribute.MAX_HEALTH) - damage


def test_subroutine_order():
    assert FireLaser(3) < Repair(1)
    assert FireLaser(1) < FireLaser(2)


def test_subroutine_eq():
    assert FireLaser(1) == FireLaser(1)
    assert FireLaser(1) != 31