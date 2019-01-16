from abc import abstractmethod

from scenes.scenes_base import Scene
from views.screen_base import Screen


class SceneArtist(object):

    @abstractmethod
    def render(self, screen: Screen, scene: Scene) -> None:
        """Generic function to render content to a screen."""
        pass
