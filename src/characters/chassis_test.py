"""Tests for the Chassis class"""
from characters.chassis import Chassis
from characters.chassis_examples import ChassisData
from characters.chassis_factory import build_chassis
from models.characters.mods_base import GenericMod, Slots
from models.characters.states import Attributes, State
from characters.subroutine_examples import FireLaser


def test_chassis_can_store_in_storage_by_default():
    storage_only_chassis = build_chassis(ChassisData({Slots.STORAGE: 1}))

    mod = GenericMod(valid_slots=Slots.HEAD)
    assert storage_only_chassis.can_store(mod)


def test_chassis_can_store_after_making_space():
    chassis = build_chassis(ChassisData({Slots.STORAGE: 1}))
    mod = GenericMod()
    chassis.attempt_store(mod)

    second_mod = GenericMod()
    assert not chassis.can_store(second_mod)
    chassis.remove_mod(mod)
    assert chassis.can_store(second_mod)
    chassis.remove_mod(second_mod)


def test_chassis_cannot_store_same_mod_twice():
    chassis = Chassis({Slots.STORAGE: 2})
    mod = GenericMod()

    chassis.attempt_store(mod)
    assert not chassis.can_store(mod)


def test_chassis_base_mod_included():
    base_mod = GenericMod(states_granted=State.ON_FIRE,
                          attribute_modifiers={Attributes.CREDITS: 3},
                          subroutines_granted=FireLaser(3))
    chassis = Chassis({}, base_mod=base_mod)

    assert len(list(chassis.all_mods())) == 1


def test_chassis_stores_in_active_slot_first():
    chassis = Chassis({Slots.ARMS: 1, Slots.STORAGE: 1})

    fire_mod = GenericMod(states_granted=State.ON_FIRE, valid_slots=Slots.ARMS)
    chassis.attempt_store(fire_mod)
    assert chassis.grants_state(State.ON_FIRE)
    assert fire_mod in chassis.all_active_mods()


def test_chassis_mods_in_storage_not_active():
    chassis = Chassis({Slots.ARMS: 1, Slots.STORAGE: 1})
    mod = GenericMod(valid_slots=Slots.CHEST)
    chassis.attempt_store(mod)
    assert mod not in chassis.all_active_mods()
    assert mod in chassis.all_mods()


def test_chassis_base_mod_is_active():
    mod = GenericMod()
    chassis = Chassis({}, base_mod=mod)
    assert mod in chassis.all_active_mods()
