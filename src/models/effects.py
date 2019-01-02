from models.mods_base import Mod
from models.player import get_player, reset_player
from models.states import AttributeType, Stateful
from scenes.scenes_base import Effect
from world.location_base import Location
from world.world import set_location, reset_world


class RestartGame(Effect):

    def execute(self) -> None:
        reset_world()
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
        get_player().attempt_pickup(self._mod)


class ChangeLocation(Effect):

    def __init__(self, location: Location) -> None:
        self._location = location

    def execute(self) -> None:
        set_location(self._location)
