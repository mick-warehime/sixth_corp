from functools import partial
from typing import Dict, Sequence, Union

from scenes.scenes_base import Scene, Resolution, Effect, SceneConstructor
from models.world import World


class DecisionOption(Resolution):

    def __init__(self, description: str,
                 effects: Union[Effect, Sequence[Effect]],
                 next_scene_fun: SceneConstructor) -> None:
        self.description = description
        if isinstance(effects, Effect):
            effects = (effects,)
        self._effects = tuple(effects)
        self._next_scene_fun = next_scene_fun

    @property
    def effects(self) -> Sequence[Effect]:
        return self._effects

    def next_scene(self, world: World) -> Scene:
        return self._next_scene_fun(world)


class DecisionScene(Scene):

    def __init__(self, prompt: str, choices: Dict[str, DecisionOption]) -> None:
        super().__init__()
        self.prompt = prompt
        self.choices = choices
        self._choice = None

    def is_resolved(self) -> bool:
        return self._choice is not None

    def make_choice(self, choice: str) -> None:
        assert choice in self.choices
        self._choice = self.choices[choice]

    def get_resolution(self) -> DecisionOption:
        return self._choice


def transition_to(
        next_scene_fun: SceneConstructor, description: str,
        effects: Union[Effect, Sequence[Effect]] = ()) -> SceneConstructor:
    """Adds a basic transition scene into another scene."""

    def scene_fun(world: World) -> DecisionScene:
        return DecisionScene(description,
                             {'1': DecisionOption('Continue', effects,
                                                  next_scene_fun)})

    return scene_fun


# This is used as a decorator for a SceneConstructor.
def from_transition(description: str,
                    effects: Union[Effect, Sequence[Effect]] = ()) -> partial:
    return partial(transition_to, description=description, effects=effects)