"""Basic interfaces for scenes, effects, and resolutions."""
import abc
from typing import Callable, Sequence


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


SceneConstructor = Callable[[], Scene]
