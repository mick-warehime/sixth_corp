"""Implementation of Scene class."""
from abstract_model import Model
from events import Event
from world import World


class Scene(Model):

    def notify(self, event: Event) -> None:
        raise NotImplementedError

    def is_resolved(self) -> bool:
        raise NotImplementedError

    def get_resolution(self):
        raise NotImplementedError


class Resolution(object):

    def execute(self, world: World) -> None:
        raise NotImplementedError

    def next_scene(self, world: World) -> Scene:
        raise NotImplementedError
