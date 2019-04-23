"""Tests for the Chassis class"""
from models.characters.chassis import Chassis
from models.characters.mods_base import SlotTypes, build_mod
from models.characters.states import Attributes, State
from models.characters.subroutine_examples import direct_damage


def test_chassis_can_store_in_storage_by_default():
    storage_only_chassis = Chassis({SlotTypes.STORAGE: 1})

    mod = build_mod(valid_slots=SlotTypes.HEAD)
    assert storage_only_chassis.can_store(mod)


def test_chassis_can_store_after_making_space():
    chassis = Chassis({SlotTypes.STORAGE: 1})
    mod = build_mod()
    chassis.attempt_store(mod)

    second_mod = build_mod()
    assert not chassis.can_store(second_mod)
    chassis.remove_mod(mod)
    assert chassis.can_store(second_mod)
    chassis.remove_mod(second_mod)


def test_chassis_cannot_store_same_mod_twice():
    chassis = Chassis({SlotTypes.STORAGE: 2})
    mod = build_mod()

    chassis.attempt_store(mod)
    assert not chassis.can_store(mod)


def test_chassis_base_mod_included():
    base_mod = build_mod(states_granted=State.ON_FIRE,
                         attribute_modifiers={Attributes.CREDITS: 3},
                         subroutines_granted=direct_damage(3))
    chassis = Chassis({}, base_mod=base_mod)

    assert len(list(chassis.all_mods())) == 1


def test_chassis_stores_in_active_slot_first():
    chassis = Chassis({SlotTypes.ARMS: 1, SlotTypes.STORAGE: 1})

    fire_mod = build_mod(states_granted=State.ON_FIRE,
                         valid_slots=SlotTypes.ARMS)
    chassis.attempt_store(fire_mod)
    assert chassis.grants_state(State.ON_FIRE)
    assert fire_mod in chassis.all_active_mods()


def test_chassis_mods_in_storage_not_active():
    chassis = Chassis({SlotTypes.ARMS: 1, SlotTypes.STORAGE: 1})
    mod = build_mod(valid_slots=SlotTypes.CHEST)
    chassis.attempt_store(mod)
    assert mod not in chassis.all_active_mods()
    assert mod in chassis.all_mods()


def test_chassis_base_mod_is_active():
    mod = build_mod()
    chassis = Chassis({}, base_mod=mod)
    assert mod in chassis.all_active_mods()
