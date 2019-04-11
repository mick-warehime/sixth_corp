from functools import partial
from typing import Dict, Sequence, Union

from data.constants import BackgroundImages
from events.events_base import EventListener, EventType, DecisionEvent
from models.scenes.scenes_base import (Effect, Resolution, Scene,
                                       SceneConstructor)


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


class DecisionScene(EventListener, Scene):
    """A Scene that is resolved by the player making a choice."""

    def __init__(self, prompt: str, choices: Dict[str, DecisionOption],
                 background_image: str = None) -> None:
        self.prompt = prompt
        super().__init__()
        self.choices = choices
        self._choice: DecisionOption = None
        if background_image is None:
            self._background_image: str = BackgroundImages.CITY.path
        else:
            self._background_image = background_image

    def notify(self, event: EventType) -> None:
        if isinstance(event, DecisionEvent) and self is event.scene:
            assert event.choice in self.choices
            self._choice = self.choices[event.choice]

    @property
    def background_image(self) -> str:
        return self._background_image

    def is_resolved(self) -> bool:
        return self._choice is not None

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
