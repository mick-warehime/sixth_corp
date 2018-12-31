from models.mods_base import Mod
from scenes.scenes_base import Effect
from models.states import AttributeType, Stateful
from models.world import World


class RestartWorld(Effect):

    def execute(self, world: World) -> None:
        world.reset()


class IncrementAttribute(Effect):

    def __init__(self, target: Stateful, attribute: AttributeType,
                 amount: int) -> None:
        self._target = target
        self._attribute = attribute
        self._amount = amount

    def execute(self, world: World) -> None:
        self._target.increment_attribute(self._attribute, self._amount)


class IncrementPlayerAttribute(Effect):

    def __init__(self, attribute: AttributeType, amount: int) -> None:
        self._attribute = attribute
        self._amount = amount

    def execute(self, world: World) -> None:
        world.player.increment_attribute(self._attribute, self._amount)


class AcquireMod(Effect):

    def __init__(self, mod: Mod) -> None:
        self._mod = mod

    def execute(self, world: World) -> None:
        world.player.inventory.store(self._mod)
