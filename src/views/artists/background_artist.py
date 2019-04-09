from data.constants import SCREEN_SIZE
from models.scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen


class BackgroundArtist(SceneArtist):
    """Draws the background image."""

    def __init__(self, scene: Scene):
        self._background_image: str = scene.background_image

    def render(self, screen: Screen, scene: Scene, layout: Layout) -> None:
        w, h = SCREEN_SIZE
        screen.render_image(self._background_image, 0, 0, w, h)
