import pytest

from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.characters.chassis import Chassis
from models.characters.chassis_examples import ChassisTypes
from models.characters.moves_base import Move
from models.characters.states import Attributes, State
from models.characters.subroutine_examples import (damage_over_time,
                                                   direct_damage)
from models.characters.subroutines_base import build_subroutine
from models.combat.combat_logic import CombatLogic


@pytest.fixture()
def player():
    # Player character with zero initial mods.
    chassis = Chassis.from_data(ChassisTypes.NO_LEGS.data)
    player = build_character(chassis, name='player')
    player.status.set_state(State.IS_PLAYER, True)
    return player


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
    starting_health = get_health()
    # Add move to stack and wait until it resolves.
    logic.start_round([move])
    for _ in range(time):
        assert get_health() == starting_health
        logic.end_round()
        assert get_cpu() == starting_cpu - cpu_used
        logic.start_round([])
        assert get_cpu() == starting_cpu - cpu_used

    # When it resolves cpu should return and HP should go down.
    logic.end_round()
    assert get_cpu() == starting_cpu
    assert get_health() == starting_health - damage


@pytest.mark.parametrize('time_to_resolve', [0, 2])
def test_move_with_multi_turn_use(player, enemy, time_to_resolve):
    num_rounds = 3
    damage_per_round = 1
    cpu_used = 1
    move = Move(damage_over_time(damage_per_round, num_rounds, cpu_used,
                                 time_to_resolve=time_to_resolve),
                player, enemy)

    logic = CombatLogic([player, enemy])

    def get_cpu():
        return player.status.get_attribute(Attributes.CPU_AVAILABLE)

    def get_health():
        return enemy.status.get_attribute(Attributes.HEALTH)

    starting_cpu = get_cpu()
    starting_health = get_health()
    # Add move to stack and wait until it resolves.
    logic.start_round([move])
    assert get_cpu() == starting_cpu

    # Wait rounds to resolve
    for _ in range(time_to_resolve):
        assert get_health() == starting_health
        logic.end_round()
        assert get_cpu() == starting_cpu - cpu_used
        logic.start_round([])

    for rnd in range(num_rounds - 1):
        assert get_health() == starting_health - rnd * damage_per_round
        logic.end_round()
        assert get_cpu() == starting_cpu - cpu_used
        assert get_health() == starting_health - (rnd + 1) * damage_per_round
        logic.start_round([])
        assert get_cpu() == starting_cpu - cpu_used

    # When it finishes cpu should return and HP should go down.
    logic.end_round()
    assert get_cpu() == starting_cpu
    assert get_health() == starting_health - num_rounds * damage_per_round


@pytest.mark.parametrize('multi_use', [True, False])
@pytest.mark.parametrize('duration', [0, 3])
@pytest.mark.parametrize('time_to_resolve', [0, 2])
def test_after_effect_occurs_at_end_of_move(player, enemy, multi_use, duration,
                                            time_to_resolve):
    after_effect_calls = []

    def after_effect(user, target):
        after_effect_calls.append(True)

    move = Move(build_subroutine(time_to_resolve=time_to_resolve,
                                 duration=duration, multi_use=multi_use,
                                 after_effect=after_effect), player, enemy)

    logic = CombatLogic([player, enemy])

    logic.start_round([move])
    assert not after_effect_calls

    for _ in range(time_to_resolve + duration):
        logic.end_round()
        assert not after_effect_calls
        logic.start_round([])
        assert not after_effect_calls

    logic.end_round()
    assert after_effect_calls


@pytest.mark.parametrize('multi_use', [True, False])
@pytest.mark.parametrize('duration', [0, 3])
@pytest.mark.parametrize('time_to_resolve', [0, 2])
def test_move_disappears_after_expected_time(player, enemy, multi_use, duration,
                                             time_to_resolve):
    move = Move(build_subroutine(time_to_resolve=time_to_resolve,
                                 duration=duration, multi_use=multi_use),
                player, enemy)

    logic = CombatLogic([player, enemy])

    logic.start_round([move])

    # A unique copy of the move is created so that it may be properly tracked.
    assert len(logic.all_moves_present()) == 1
    move = logic.all_moves_present()[0]

    for _ in range(time_to_resolve + duration):
        logic.end_round()
        assert move in logic.all_moves_present()
        logic.start_round([])
        assert move in logic.all_moves_present()

    logic.end_round()
    assert move not in logic.all_moves_present()
