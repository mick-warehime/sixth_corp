"""Tests of status.py"""
import pytest

from models.characters.states import Attributes, Skills, State, StatusEffect
from models.characters.status import BasicStatus


def test_basic_status_states():
    status = BasicStatus()

    state = State.ON_FIRE
    assert not status.has_state(state)

    status.set_state(state, True)
    assert status.has_state(state)

    status.set_state(state, False)
    assert not status.has_state(state)

    status.set_state(state, False)
    assert not status.has_state(state)


@pytest.mark.parametrize('att', [Attributes.HEALTH, Skills.MECHANICS])
@pytest.mark.parametrize('bound', [2, Attributes.MAX_HEALTH, lambda: 2])
def test_basis_status_attribute_increment_bounds(att, bound):
    status = BasicStatus()

    att = Attributes.HEALTH

    assert status.get_attribute(att) == 0

    status.set_attribute_bounds(att, 0, bound)

    if isinstance(bound, int):
        expected = bound
    elif isinstance(bound, Attributes):
        expected = status.get_attribute(bound)
    else:
        assert callable(bound)
        expected = bound()

    status.increment_attribute(att, expected + 1)

    actual = status.get_attribute(att)
    assert actual == expected


def test_status_effect_adds_state():
    status = BasicStatus()

    state = State.ON_FIRE
    fire_effect = StatusEffect.build('fire', states_granted=state)

    assert not status.has_state(state)
    status.add_status_effect(fire_effect)

    assert status.has_state(state)


def test_status_effect_prevents_state():
    status = BasicStatus()

    state = State.ON_FIRE
    status.set_state(state, True)
    assert status.has_state(state)

    no_fire = StatusEffect.build('no fire', states_prevented=state)
    status.add_status_effect(no_fire)

    assert not status.has_state(state)
    status.set_state(state, True)
    assert not status.has_state(state)


def test_status_effect_prevents_status_effect_state():
    status = BasicStatus()

    state = State.ON_FIRE

    fire_effect = StatusEffect.build('fire', states_granted=state)
    status.add_status_effect(fire_effect)

    no_fire = StatusEffect.build('no fire', states_prevented=state)
    status.add_status_effect(no_fire)

    assert not status.has_state(state)
    status.remove_status_effect(no_fire)
    assert status.has_state(state)


def test_status_effect_attribute_increments_stack():
    status = BasicStatus()

    att = Attributes.HEALTH
    assert status.get_attribute(att) == 0

    increment = 1
    buff_hp = StatusEffect.build(attribute_modifiers={att: increment})

    expected = increment
    status.add_status_effect(buff_hp)
    assert status.get_attribute(att) == expected

    status.add_status_effect(buff_hp)
    expected += increment
    assert status.get_attribute(att) == expected


def test_status_effect_attribute_increments_stay_in_bounds():
    status = BasicStatus()

    att = Attributes.HEALTH
    lower, initial, upper = 0, 1, 2
    status.increment_attribute(att, initial)

    assert status.get_attribute(att) == initial
    status.set_attribute_bounds(att, lower, upper)

    increment = 100
    minus_hp = StatusEffect.build(attribute_modifiers={att: -increment})
    plus_hp = StatusEffect.build(attribute_modifiers={att: increment})

    status.add_status_effect(minus_hp)
    assert status.get_attribute(att) == lower
    status.add_status_effect(plus_hp)  # cancels other buff
    assert status.get_attribute(att) == initial
    status.add_status_effect(plus_hp)
    assert status.get_attribute(att) == upper

    assert len(status.active_effects()) == 3


def test_status_effect_partial_bounds():
    status = BasicStatus()

    att = Attributes.HEALTH
    lower, initial, upper = None, 1, 2
    status.increment_attribute(att, initial)

    assert status.get_attribute(att) == initial
    status.set_attribute_bounds(att, lower, upper)

    status.increment_attribute(att, upper + 1)
    assert status.get_attribute(att) == upper

    status.increment_attribute(att, -upper - 1)
    assert status.get_attribute(att) == -1
