from models.inventory import BasicInventory
from models.mod_examples import HullPlating, CamouflagePaint, HelmOfBeingOnFire


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
