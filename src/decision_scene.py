from typing import Dict, Sequence

from effects import ChangeSceneName
from scenes_base import Scene, Resolution, Effect
from world import World


class DecisionOption(Resolution):

    def __init__(self, name: str) -> None:
        self._effects = (ChangeSceneName(name),)
        self.name = name

    @property
    def effects(self) -> Sequence[Effect]:
        return self._effects

    def next_scene(self, world: World) -> Scene:
        pass


class DecisionScene(Scene):

    def __init__(self, prompt: str, choices: Dict[str, DecisionOption]):
        super().__init__()
        self.prompt = prompt
        self.choices = choices

    def is_resolved(self) -> bool:
        pass

    def get_resolution(self):
        pass
