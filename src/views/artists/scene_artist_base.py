import abc

from models.scenes.scenes_base import Scene
from views.pygame_screen import Screen


class SceneArtist(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, screen: Screen, scene: Scene) -> None:
        """Generic function to render content to a screen."""
