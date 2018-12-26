from scenes_base import Effect
from world import World


class ChangeSceneName(Effect):

    def __init__(self, name: str) -> None:
        self._name = name

    def execute(self, world: World) -> None:
        world.current_scene = self._name


class IncrementSceneCount(Effect):

    def execute(self, world: World) -> None:
        world.scene_count += 1
