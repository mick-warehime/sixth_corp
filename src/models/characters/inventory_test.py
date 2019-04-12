from functools import partial

import pytest

from models.characters.chassis import Chassis
from models.characters.inventory import BasicInventory
from models.characters.mods_base import GenericMod, Slots
from models.characters.states import Attributes, State
from models.characters.subroutine_examples import FireLaser, Repair

factories = (BasicInventory, partial(Chassis, {Slots.STORAGE: 4}))


@pytest.mark.parametrize('make_inventory', factories)
def test_inventory_storage_sizes(make_inventory):
    inventory = make_inventory()

    assert inventory.can_store(GenericMod())
    assert len(list(inventory.all_mods())) == 0
    inventory.attempt_store(GenericMod())
    assert len(list(inventory.all_mods())) == 1
    inventory.attempt_store(GenericMod())
    assert len(list(inventory.all_mods())) == 2


@pytest.mark.parametrize('make_inventory', factories)
def test_basic_inventory_removal(make_inventory):
    mod = GenericMod()

    inventory = make_inventory()

    inventory.attempt_store(mod)
    inventory.remove_mod(mod)

    assert len(list(inventory.all_mods())) == 0


@pytest.mark.parametrize('make_inventory', factories)
def test_basic_inventory_mods(make_inventory):
    inventory = make_inventory()

    inventory.attempt_store(GenericMod(subroutines_granted=FireLaser(2)))
    inventory.attempt_store(GenericMod(states_granted=State.ON_FIRE,
                                       attribute_modifiers={
                                           Attributes.MAX_HEALTH: 2}))
    inventory.attempt_store(
        GenericMod(attribute_modifiers={Attributes.MAX_HEALTH: 1}))
    inventory.attempt_store(
        GenericMod(attribute_modifiers={Attributes.MAX_HEALTH: 3},
                   subroutines_granted=Repair(3)))

    mods = list(inventory.mods(lambda x: bool(x.subroutines_granted()),
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

    assert inventory.total_modifier(Attributes.MAX_HEALTH) == 0
    inventory.attempt_store(
        GenericMod(attribute_modifiers={Attributes.MAX_HEALTH: 5}))
    assert inventory.total_modifier(Attributes.MAX_HEALTH) == 5
    inventory.attempt_store(
        GenericMod(attribute_modifiers={Attributes.MAX_HEALTH: 3}))
    assert inventory.total_modifier(Attributes.MAX_HEALTH) == 8


def test_state_granted():
    inventory = BasicInventory()

    assert not inventory.grants_state(State.ON_FIRE)
    inventory.attempt_store(GenericMod(states_granted=State.ON_FIRE))
    assert inventory.grants_state(State.ON_FIRE)


def test_inventory_all_subroutines():
    inventory = BasicInventory()

    assert not inventory.all_subroutines()

    fire_laser = FireLaser(1)
    inventory.attempt_store(GenericMod(subroutines_granted=fire_laser))
    assert (fire_laser,) == tuple(inventory.all_subroutines())

    repair = Repair(1)
    inventory.attempt_store(GenericMod(subroutines_granted=repair))
    assert tuple(inventory.all_subroutines()) == (fire_laser, repair)
