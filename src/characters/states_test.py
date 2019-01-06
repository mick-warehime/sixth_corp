"""Tests for states.py"""

from characters.states import Attribute, BasicStatus, State


def test_str_methods():
    assert str(State.ON_FIRE) == 'on fire'
    assert str(Attribute.HEALTH) == 'health'


def test_basic_status_attribute_bounds():
    status = BasicStatus()
    health_min = -5
    health_max = 10
    status.set_attribute(Attribute.MAX_HEALTH, health_max)
    status.set_attribute_bounds(Attribute.HEALTH, health_min,
                                Attribute.MAX_HEALTH)

    assert status.get_attribute(Attribute.HEALTH) == 0
    status.set_attribute(Attribute.HEALTH, health_max + 100)
    assert status.get_attribute(Attribute.HEALTH) == health_max
    status.increment_attribute(Attribute.HEALTH, 100)
    assert status.get_attribute(Attribute.HEALTH) == health_max
    status.increment_attribute(Attribute.HEALTH, -health_max + health_min - 5)
    assert status.get_attribute(Attribute.HEALTH) == health_min
    status.set_attribute(Attribute.HEALTH, health_min - 10)
    assert status.get_attribute(Attribute.HEALTH) == health_min
