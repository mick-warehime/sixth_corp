from functools import partial
from typing import (Any, Dict, List, NamedTuple, Optional, Sequence, Tuple,
                    Union)

from data.colors import GREEN, ColorType
from data.constants import SCREEN_SIZE, BackgroundImages
from events.events_base import (BasicEvents, DecisionEvent, EventListener,
                                EventType)
from models.scenes.inventory_scene import InventoryScene
from models.scenes.layouts import Layout
from models.scenes.scenes_base import (BasicResolution, EffectType, Resolution,
                                       Scene, SceneConstructor)


class DecisionOption(Resolution):
    """Resolves by calling a scene constructor function."""

    def __init__(self, description: str, next_scene_fun: SceneConstructor,
                 effects: Union[EffectType, Sequence[EffectType]] = ()) -> None:
        self.description = description
        if callable(effects):
            effects = (effects,)
        self._effects = tuple(effects)
        self._next_scene_fun = next_scene_fun

    @property
    def effects(self) -> Sequence[EffectType]:
        return self._effects

    def next_scene(self) -> Scene:
        return self._next_scene_fun()


class DecisionInfo(NamedTuple):
    """All information needed to render some decision text."""
    text: str
    key: Optional[str]
    centered: bool
    is_prompt: bool = False
    color: ColorType = GREEN


class DecisionScene(EventListener, Scene):
    """A Scene that is resolved by the player making a choice."""

    def __init__(self, prompt: str, choices: Dict[str, DecisionOption],
                 background_image: str = None,
                 inventory_available: bool = True,
                 centered_prompt: bool = False,
                 centered_choices: bool = False) -> None:
        self._prompt = prompt
        super().__init__()
        self.choices = choices
        self._choice: Optional[Resolution] = None
        if background_image is None:
            self._background_image: str = BackgroundImages.CITY.path
        else:
            self._background_image = background_image
        self._inventory_available = inventory_available

        self._layout: Layout = self._define_layout(centered_prompt,
                                                   centered_choices)

    def notify(self, event: EventType) -> None:
        if isinstance(event, DecisionEvent) and self is event.scene:
            assert event.choice in self.choices
            self._choice = self.choices[event.choice]
        elif event == BasicEvents.INVENTORY:
            self._select_inventory()

    @property
    def layout(self) -> Layout:
        return self._layout

    @property
    def inventory_available(self) -> bool:
        return self._inventory_available

    def _select_inventory(self) -> None:
        """Chooses the inventory scene as the scene resolution."""

        if self.inventory_available:
            def reload_self() -> DecisionScene:
                # We must reset choice to None so that we don't immediately
                # bounce back to the inventory scene when self is reloaded.
                self._choice = None
                return self

            def inv_scene() -> InventoryScene:
                return InventoryScene(reload_self)

            self._choice = BasicResolution(inv_scene)

    @property
    def background_image(self) -> str:
        return self._background_image

    def is_resolved(self) -> bool:
        return self._choice is not None

    def get_resolution(self) -> Resolution:
        assert self._choice is not None
        return self._choice

    def __str__(self) -> str:
        max_char = min(len(self._prompt), 40)
        return 'DecisionScene({}...)'.format(self._prompt[:max_char])

    def _define_layout(self, centered_prompt: bool,
                       centered_choices: bool) -> Layout:
        # Layout is composed of the scene prompt/description, below which is
        # the list of decisions.

        prompt = DecisionInfo(self._prompt, None, centered_prompt,
                              is_prompt=True)

        choice_weight = 4
        choice_elems: List[Tuple[Any, int]] = [
            (DecisionInfo(c.description, k, centered_choices), 1)
            for k, c in self.choices.items()]
        if len(choice_elems) < choice_weight:
            choice_elems.append((None, choice_weight - len(choice_elems)))
        choice_layout = Layout(choice_elems)
        choice_layout = Layout([(None, 1), (choice_layout, 8), (None, 1)],
                               'horizontal')

        middle = Layout(
            [(None, 2), (prompt, 4), (None, 2), (choice_layout, choice_weight),
             (None, 2)])

        return Layout([(None, 1), (middle, 5), (None, 1)],
                      direction='horizontal', dimensions=SCREEN_SIZE)


def transition_to(
        next_scene_fun: SceneConstructor, description: str,
        effects: Union[EffectType, Sequence[EffectType]] = ()
) -> SceneConstructor:
    """Adds a basic transition scene into another scene."""

    def scene_fun() -> DecisionScene:
        return DecisionScene(description,
                             {'1': DecisionOption('Continue', next_scene_fun,
                                                  effects)},
                             inventory_available=False, centered_choices=True)

    return scene_fun


# This is used as a decorator for a SceneConstructor.
def from_transition(description: str,
                    effects: Union[
                        EffectType, Sequence[EffectType]] = ()) -> partial:
    return partial(transition_to, description=description, effects=effects)
