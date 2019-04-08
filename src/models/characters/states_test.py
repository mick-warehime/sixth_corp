"""Tests for states.py"""

from models.characters.states import Attributes, State
from models.characters.status import BasicStatus


def test_str_methods():
    assert str(State.ON_FIRE) == 'on fire'
    assert str(Attributes.HEALTH) == 'health'


def test_basic_status_attribute_bounds():
    status = BasicStatus()
    health_min = -5
    health_max = 10
    status.set_attribute(Attributes.MAX_HEALTH, health_max)
    status.set_attribute_bounds(Attributes.HEALTH, health_min,
                                Attributes.MAX_HEALTH)

    assert status.get_attribute(Attributes.HEALTH) == 0
    status.set_attribute(Attributes.HEALTH, health_max + 100)
    assert status.get_attribute(Attributes.HEALTH) == health_max
    status.increment_attribute(Attributes.HEALTH, 100)
    assert status.get_attribute(Attributes.HEALTH) == health_max
    status.increment_attribute(Attributes.HEALTH, -health_max + health_min - 5)
    assert status.get_attribute(Attributes.HEALTH) == health_min
    status.set_attribute(Attributes.HEALTH, health_min - 10)
    assert status.get_attribute(Attributes.HEALTH) == health_min
