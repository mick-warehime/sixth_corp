import abc

from scenes.scenes_base import Scene
from views.layouts import Layout
from views.screen_base import Screen


class SceneArtist(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, screen: Screen, scene: Scene, layout: Layout) -> None:
        """Generic function to render content to a screen."""
