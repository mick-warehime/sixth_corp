from functools import partial

import pytest

from characters.ability_examples import FireLaser, Repair
from characters.chassis import Chassis, Slots, TEMP_DEFAULT_SLOT
from characters.inventory import BasicInventory
from characters.mod_examples import (BasicLaser, CamouflagePaint,
                                     HelmOfBeingOnFire, HullPlating)
from characters.mods_base import GenericMod
from characters.states import Attribute, State

factories = (BasicInventory, partial(Chassis, {TEMP_DEFAULT_SLOT: 4}))


@pytest.mark.parametrize('make_inventory', factories)
def test_inventory_storage_sizes(make_inventory):
    inventory = make_inventory()

    assert inventory.can_store(HullPlating())
    assert len(list(inventory.all_mods())) == 0
    inventory.store(HullPlating())
    assert len(list(inventory.all_mods())) == 1
    inventory.store(HullPlating())
    assert len(list(inventory.all_mods())) == 2


def test_chassis_cannot_store_same_mod_twice():
    chassis = Chassis({TEMP_DEFAULT_SLOT: 2})
    mod = HullPlating()

    chassis.store(mod)
    assert not chassis.can_store(mod)


def test_chassis_cannot_store_when_full():
    chassis = Chassis({TEMP_DEFAULT_SLOT: 2})

    chassis.store(HullPlating())
    chassis.store(HullPlating())
    assert not chassis.can_store(HullPlating())


@pytest.mark.parametrize('make_inventory', factories)
def test_basic_inventory_removal(make_inventory):
    mod = HullPlating()

    inventory = make_inventory()

    inventory.store(mod)
    inventory.remove(mod)

    assert len(list(inventory.all_mods())) == 0


@pytest.mark.parametrize('make_inventory', factories)
def test_basic_inventory_mods(make_inventory):
    inventory = make_inventory()

    inventory.store(HullPlating())
    inventory.store(HullPlating())
    inventory.store(CamouflagePaint())
    inventory.store(HelmOfBeingOnFire())

    mods = list(inventory.mods(lambda x: isinstance(x, HullPlating)))
    assert len(mods) == 2

    mods = list(inventory.mods(lambda x: bool(x.states_granted())))
    assert len(mods) == 1

    mods = list(inventory.mods(lambda x: bool(x.attribute_modifiers())))
    assert len(mods) == 3


def test_total_modifier():
    inventory = BasicInventory()

    assert inventory.total_modifier(Attribute.MAX_HEALTH) == 0
    inventory.store(HullPlating(health_bonus=5))
    assert inventory.total_modifier(Attribute.MAX_HEALTH) == 5
    inventory.store(HullPlating(health_bonus=3))
    assert inventory.total_modifier(Attribute.MAX_HEALTH) == 8


def test_state_granted():
    inventory = BasicInventory()

    assert not inventory.grants_state(State.ON_FIRE)
    inventory.store(HelmOfBeingOnFire())
    assert inventory.grants_state(State.ON_FIRE)


def test_inventory_all_abilities():
    inventory = BasicInventory()

    assert not inventory.all_abilities()

    inventory.store(BasicLaser(1))
    assert (FireLaser(1),) == tuple(inventory.all_abilities())

    inventory.store(GenericMod(abilities_granted=Repair(1)))
    assert tuple(inventory.all_abilities()) == (FireLaser(1), Repair(1))
