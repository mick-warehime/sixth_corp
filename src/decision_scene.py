from typing import Dict

from events import Event, EventManager
from scenes import Scene, Resolution
from world import World


class DecisionOption(Resolution):

    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, world: World) -> None:
        world.current_scene = self.name

    def next_scene(self, world: World) -> Scene:
        pass


class DecisionScene(Scene):

    def __init__(self, choices: Dict[str, DecisionOption]):
        super().__init__()
        self._choices = choices

    def is_resolved(self) -> bool:
        pass

    def notify(self, event: Event) -> None:
        pass

    def get_resolution(self):
        pass
