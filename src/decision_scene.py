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
        self._choice = None

    def is_resolved(self) -> bool:
        return self._choice is not None

    def make_choice(self, choice: str):
        assert choice in self.choices
        self._choice = self.choices[choice]

    def get_resolution(self):
        return self._choice
