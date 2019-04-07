from functools import partial
from typing import Dict, Sequence, Union

from models.scenes.scenes_base import Effect, Resolution, Scene, SceneConstructor


class DecisionOption(Resolution):
    """Resolves by calling a scene constructor function."""

    def __init__(self, description: str, next_scene_fun: SceneConstructor,
                 effects: Union[Effect, Sequence[Effect]] = ()) -> None:
        self.description = description
        if isinstance(effects, Effect):
            effects = (effects,)
        self._effects = tuple(effects)
        self._next_scene_fun = next_scene_fun

    @property
    def effects(self) -> Sequence[Effect]:
        return self._effects

    def next_scene(self) -> Scene:
        return self._next_scene_fun()


class DecisionScene(Scene):
    """A Scene that is resolved by the player making a choice."""

    def __init__(self, prompt: str, choices: Dict[str, DecisionOption]) -> None:
        super().__init__()
        self.prompt = prompt
        self.choices = choices
        self._choice: DecisionOption = None

    def is_resolved(self) -> bool:
        return self._choice is not None

    def make_choice(self, choice: str) -> None:
        assert choice in self.choices
        self._choice = self.choices[choice]

    def get_resolution(self) -> DecisionOption:
        return self._choice

    def __str__(self) -> str:
        max_char = min(len(self.prompt), 40)
        return 'DecisionScene({}...)'.format(self.prompt[:max_char])


def transition_to(
        next_scene_fun: SceneConstructor, description: str,
        effects: Union[Effect, Sequence[Effect]] = ()) -> SceneConstructor:
    """Adds a basic transition scene into another scene."""

    def scene_fun() -> DecisionScene:
        return DecisionScene(description,
                             {'1': DecisionOption('Continue', next_scene_fun,
                                                  effects)})

    return scene_fun


# This is used as a decorator for a SceneConstructor.
def from_transition(description: str,
                    effects: Union[Effect, Sequence[Effect]] = ()) -> partial:
    return partial(transition_to, description=description, effects=effects)
