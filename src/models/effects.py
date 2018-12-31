from models.mods_base import Mod
from models.world import get_world
from scenes.scenes_base import Effect
from models.states import AttributeType, Stateful


class RestartWorld(Effect):

    def execute(self) -> None:
        get_world().reset()


class IncrementAttribute(Effect):

    def __init__(self, target: Stateful, attribute: AttributeType,
                 amount: int) -> None:
        self._target = target
        self._attribute = attribute
        self._amount = amount

    def execute(self) -> None:
        self._target.increment_attribute(self._attribute, self._amount)


class IncrementPlayerAttribute(Effect):

    def __init__(self, attribute: AttributeType, amount: int) -> None:
        self._attribute = attribute
        self._amount = amount

    def execute(self) -> None:
        world = get_world()
        world.player.increment_attribute(self._attribute, self._amount)


class AcquireMod(Effect):

    def __init__(self, mod: Mod) -> None:
        self._mod = mod

    def execute(self) -> None:
        world = get_world()
        world.player.inventory.store(self._mod)
