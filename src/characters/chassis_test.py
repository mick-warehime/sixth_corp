"""Tests for the Chassis class"""
from characters.ability_examples import FireLaser
from characters.chassis import Chassis
from characters.chassis_examples import ChassisData
from characters.chassis_factory import build_chassis
from characters.mods_base import GenericMod, Slots
from characters.states import Attribute, State


def test_chassis_can_store_in_storage_by_default():
    storage_only_chassis = build_chassis(ChassisData({Slots.STORAGE: 1}))

    mod = GenericMod(valid_slots=Slots.HEAD)
    assert storage_only_chassis.can_store(mod)


def test_chassis_can_store_after_making_space():
    chassis = build_chassis(ChassisData({Slots.STORAGE: 1}))
    mod = GenericMod()
    chassis.store(mod)

    second_mod = GenericMod()
    assert not chassis.can_store(second_mod)
    chassis.remove_mod(mod)
    assert chassis.can_store(second_mod)
    chassis.remove_mod(second_mod)


def test_chassis_cannot_store_same_mod_twice():
    chassis = Chassis({Slots.STORAGE: 2})
    mod = GenericMod()

    chassis.store(mod)
    assert not chassis.can_store(mod)


def test_chassis_base_mod_included():
    base_mod = GenericMod(states_granted=State.ON_FIRE,
                          attribute_modifiers={Attribute.CREDITS: 3},
                          abilities_granted=FireLaser(3))
    chassis = Chassis({}, base_mod=base_mod)

    assert len(list(chassis.all_mods())) == 1
