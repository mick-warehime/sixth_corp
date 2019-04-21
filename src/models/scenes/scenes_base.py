"""Basic interfaces for scenes, effects, and resolutions."""
import abc
from typing import Callable, Sequence, Tuple


class Scene(metaclass=abc.ABCMeta):
    """Basic representation of a game scene."""

    @abc.abstractmethod
    def is_resolved(self) -> bool:
        """Whether the scene is resolved."""

    @abc.abstractmethod
    def get_resolution(self) -> 'Resolution':
        """The resolution to the scene (if is_resolved is True)."""

    @property
    @abc.abstractmethod
    def background_image(self) -> str:
        """The path to the background image."""


class Effect(object):
    """Implements some action on the game world."""

    def execute(self) -> None:
        raise NotImplementedError


class Resolution(object):
    """Determines the next scene."""

    def next_scene(self) -> Scene:
        raise NotImplementedError

    @property
    def effects(self) -> Sequence[Effect]:
        """These are implemented when the resolution occurs."""
        raise NotImplementedError


class BasicResolution(Resolution):

    def __init__(self, scene_fun: Callable[[], Scene],
                 effect_seq: Tuple[Effect, ...] = ()) -> None:
        self._scene_fun = scene_fun
        self._effect_seq = effect_seq

    def next_scene(self) -> Scene:
        return self._scene_fun()

    @property
    def effects(self) -> Sequence[Effect]:
        return self._effect_seq


SceneConstructor = Callable[[], Scene]
