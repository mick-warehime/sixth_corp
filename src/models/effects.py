from models.mods_base import Mod
from models.player import get_player, reset_player
from models.world import get_world
from scenes.scenes_base import Effect
from models.states import AttributeType, Stateful


class RestartGame(Effect):

    def execute(self) -> None:
        get_world().reset()
        reset_player()


class IncrementAttribute(Effect):

    def __init__(self, target: Stateful, attribute: AttributeType,
                 amount: int) -> None:
        self._target = target
        self._attribute = attribute
        self._amount = amount

    def execute(self) -> None:
        self._target.increment_attribute(self._attribute, self._amount)


class AcquireMod(Effect):

    def __init__(self, mod: Mod) -> None:
        self._mod = mod

    def execute(self) -> None:
        get_player().inventory.store(self._mod)
