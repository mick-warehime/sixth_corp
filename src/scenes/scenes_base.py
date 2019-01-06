"""Basic interfaces for scenes, effects, and resolutions."""
from typing import Callable, Sequence


class Scene(object):
    """Basic representation of a game scene."""

    def is_resolved(self) -> bool:
        raise NotImplementedError

    def get_resolution(self) -> 'Resolution':
        raise NotImplementedError


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
        raise NotImplementedError


SceneConstructor = Callable[[], Scene]
