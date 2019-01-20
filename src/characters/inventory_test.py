from functools import partial

import pytest

from characters.ability_examples import FireLaser, Repair
from characters.chassis import Chassis
from characters.inventory import BasicInventory
from characters.mods_base import GenericMod, Slots
from characters.states import Attribute, State

factories = (BasicInventory, partial(Chassis, {Slots.STORAGE: 4}))


@pytest.mark.parametrize('make_inventory', factories)
def test_inventory_storage_sizes(make_inventory):
    inventory = make_inventory()

    assert inventory.can_store(GenericMod())
    assert len(list(inventory.all_mods())) == 0
    inventory.store(GenericMod())
    assert len(list(inventory.all_mods())) == 1
    inventory.store(GenericMod())
    assert len(list(inventory.all_mods())) == 2


@pytest.mark.parametrize('make_inventory', factories)
def test_basic_inventory_removal(make_inventory):
    mod = GenericMod()

    inventory = make_inventory()

    inventory.store(mod)
    inventory.remove_mod(mod)

    assert len(list(inventory.all_mods())) == 0


@pytest.mark.parametrize('make_inventory', factories)
def test_basic_inventory_mods(make_inventory):
    inventory = make_inventory()

    inventory.store(GenericMod(abilities_granted=FireLaser(2)))
    inventory.store(GenericMod(states_granted=State.ON_FIRE,
                               attribute_modifiers={Attribute.MAX_HEALTH: 2}))
    inventory.store(GenericMod(attribute_modifiers={Attribute.MAX_HEALTH: 1}))
    inventory.store(GenericMod(attribute_modifiers={Attribute.MAX_HEALTH: 3},
                               abilities_granted=Repair(3)))

    mods = list(inventory.mods(lambda x: bool(x.abilities_granted()),
                               active_only=False))
    assert len(mods) == 2

    mods = list(
        inventory.mods(lambda x: bool(x.states_granted()), active_only=False))
    assert len(mods) == 1

    mods = list(inventory.mods(lambda x: bool(x.attribute_modifiers()),
                               active_only=False))
    assert len(mods) == 3


def test_total_modifier():
    inventory = BasicInventory()

    assert inventory.total_modifier(Attribute.MAX_HEALTH) == 0
    inventory.store(GenericMod(attribute_modifiers={Attribute.MAX_HEALTH: 5}))
    assert inventory.total_modifier(Attribute.MAX_HEALTH) == 5
    inventory.store(GenericMod(attribute_modifiers={Attribute.MAX_HEALTH: 3}))
    assert inventory.total_modifier(Attribute.MAX_HEALTH) == 8


def test_state_granted():
    inventory = BasicInventory()

    assert not inventory.grants_state(State.ON_FIRE)
    inventory.store(GenericMod(states_granted=State.ON_FIRE))
    assert inventory.grants_state(State.ON_FIRE)


def test_inventory_all_abilities():
    inventory = BasicInventory()

    assert not inventory.all_abilities()

    inventory.store(GenericMod(abilities_granted=FireLaser(1)))
    assert (FireLaser(1),) == tuple(inventory.all_abilities())

    inventory.store(GenericMod(abilities_granted=Repair(1)))
    assert tuple(inventory.all_abilities()) == (FireLaser(1), Repair(1))
