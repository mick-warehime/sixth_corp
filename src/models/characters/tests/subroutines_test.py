import pytest

from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis_examples import ChassisTypes
from models.characters.conditions import at_full_health
from models.characters.states import Attributes, State
from models.characters.subroutine_examples import direct_damage, repair
from models.characters.subroutines_base import build_subroutine


@pytest.fixture()
def character():
    return build_character(data=CharacterData(ChassisTypes.NO_LEGS.data))


def test_repair_subroutine(character: Character):
    repair_sub = repair(3)
    assert repair_sub.can_use(character, character)
    character.status.increment_attribute(Attributes.HEALTH, -1)
    assert repair_sub.can_use(character, character)
    repair_sub.use(character, character)
    assert at_full_health(character)


def test_fire_laser(character):
    damage = 3
    fire_laser = direct_damage(damage)
    other_char = build_character(data=CharacterData(ChassisTypes.NO_LEGS.data))
    other_char.status.set_state(State.IS_PLAYER, True)

    assert not fire_laser.can_use(character, character)
    assert fire_laser.can_use(character, other_char)
    fire_laser.use(character, other_char)
    value = other_char.status.get_attribute
    assert value(Attributes.HEALTH) == value(Attributes.MAX_HEALTH) - damage


def test_subroutine_eq():
    assert build_subroutine() != build_subroutine()
    sub = build_subroutine()
    assert sub == sub
    assert sub != sub.copy()
