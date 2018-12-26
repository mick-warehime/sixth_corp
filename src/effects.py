from scenes_base import Effect
from states import Attribute
from world import World


class IncrementSceneCount(Effect):

    def execute(self, world: World) -> None:
        world.scene_count += 1


class RestartWorld(Effect):

    def execute(self, world: World) -> None:
        world.reset()


class IncrementPlayerAttribute(Effect):

    def __init__(self, attribute: Attribute, amount: int) -> None:
        self._attribute = attribute
        self._amount = amount

    def execute(self, world: World) -> None:
        world.player.increment_attribute(self._attribute, self._amount)
