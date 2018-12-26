"""Implementation of Scene class."""
from events import Event, EventListener
from world import World


class Scene(EventListener):

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
