from abc import abstractmethod
from typing import Any

from views.screen_base import Screen


class SceneArtist(object):

    @abstractmethod
    def render(self, screen: Screen, scene: Any) -> None:  # type: ignore
        """Generic function to render content to a screen."""
        pass
