from models.ability_examples import FireLaser, Repair
from models.inventory import BasicInventory
from models.mod_examples import HullPlating, CamouflagePaint, HelmOfBeingOnFire, \
    BasicLaser
from models.mods_base import GenericMod
from models.states import Attribute, State


def test_basic_inventory_storage_sizes():
    mod = HullPlating()

    inventory = BasicInventory()

    assert inventory.can_store(mod)
    assert len(list(inventory.all_mods())) == 0
    inventory.store(mod)
    assert len(list(inventory.all_mods())) == 1
    inventory.store(mod)
    assert len(list(inventory.all_mods())) == 2


def test_basic_inventory_removal():
    mod = HullPlating()

    inventory = BasicInventory()

    inventory.store(mod)
    inventory.store(mod)
    inventory.remove(mod)

    assert len(list(inventory.all_mods())) == 1


def test_basic_inventory_mods():
    inventory = BasicInventory()

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
