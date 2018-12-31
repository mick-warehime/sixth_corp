from models.character_base import Character
from models.mods_base import Mod
from models.player import Player
from models.states import AttributeType, Stateful
from scenes.scenes_base import Effect


class RestartWorld(Effect):

    def execute(self) -> None:
        Player.reset()


class IncrementAttribute(Effect):

    def __init__(self, target: Stateful, attribute: AttributeType,
                 amount: int) -> None:
        self._target = target
        self._attribute = attribute
        self._amount = amount

    def execute(self) -> None:
        self._target.increment_attribute(self._attribute, self._amount)


class AcquireMod(Effect):

    def __init__(self, target: Character, mod: Mod) -> None:
        self._target = target
        self._mod = mod

    def execute(self) -> None:
        self._target.add_mod(self._mod)
