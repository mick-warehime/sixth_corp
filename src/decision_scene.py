from typing import Dict, Sequence, Union

from scenes_base import Scene, Resolution, Effect
from world import World


class DecisionOption(Resolution):

    def __init__(self, description: str,
                 effects: Union[Effect, Sequence[Effect]]) -> None:
        self.description = description
        if isinstance(effects, Effect):
            effects = (effects,)
        self._effects = tuple(effects)

    @property
    def effects(self) -> Sequence[Effect]:
        return self._effects

    def next_scene(self, world: World) -> Scene:
        return DecisionScene('TEST', {'a': DecisionOption('choice', ())})


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
