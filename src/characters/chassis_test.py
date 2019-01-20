"""Tests for the Chassis class"""
from characters.chassis_examples import ChassisData
from characters.chassis_factory import build_chassis
from characters.mods_base import Slots, GenericMod


def test_chassis_can_store_in_storage_by_default():
    storage_only_chassis = build_chassis(ChassisData({Slots.STORAGE: 1}))

    mod = GenericMod(valid_slots=Slots.HEAD)
    assert storage_only_chassis.can_store(mod)


def test_chassis_cannot_store_when_full():
    chassis = build_chassis(ChassisData({Slots.STORAGE: 1}))
    chassis.store(GenericMod())

    assert not chassis.can_store(GenericMod())
