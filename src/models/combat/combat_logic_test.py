import pytest

from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.chassis import Chassis
from models.characters.chassis_examples import ChassisTypes
from models.characters.mods_base import build_mod
from models.characters.moves_base import Move
from models.characters.states import Attributes
from models.characters.subroutine_examples import direct_damage
from models.combat.combat_logic import CombatLogic


@pytest.fixture()
def player():
    # Player character with zero initial mods.
    chassis = Chassis.from_data(ChassisTypes.NO_LEGS.data)
    return build_character(chassis, name='player')


@pytest.fixture()
def enemy():
    return build_character(data=CharacterTypes.DRONE.data)


def test_combat_logic_initializes_cpu(player, enemy):
    chars = [player, enemy]
    for char in chars:
        cpu = char.status.get_attribute(Attributes.CPU_AVAILABLE)
        char.status.increment_attribute(Attributes.CPU_AVAILABLE, -cpu)

    CombatLogic(chars)

    for char in chars:
        actual = char.status.get_attribute(Attributes.CPU_AVAILABLE)
        expected = char.status.get_attribute(Attributes.MAX_CPU)
        assert actual == expected


def test_direct_move_removes_and_returns_cpu(player, enemy):
    cpu_used = 2
    time = 3
    damage = 1
    move = Move(direct_damage(damage, cpu_slots=cpu_used, time_to_resolve=time),
                player, enemy)

    logic = CombatLogic([player, enemy])

    def get_cpu():
        return player.status.get_attribute(Attributes.CPU_AVAILABLE)

    def get_health():
        return enemy.status.get_attribute(Attributes.HEALTH)

    starting_cpu = get_cpu()
    starting_HP = get_health()
    # Add move to stack and wait until it resolves.
    logic.start_round([move])
    for _ in range(time):
        assert get_cpu() == starting_cpu - cpu_used
        assert get_health() == starting_HP
        logic.end_round()
        assert get_cpu() == starting_cpu - cpu_used
        logic.start_round([])

    # When it resolves cpu should return and HP should go down.
    logic.end_round()
    assert get_cpu() == starting_cpu
    assert get_health() == starting_HP - damage
