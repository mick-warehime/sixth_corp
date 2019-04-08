from data.constants import SCREEN_SIZE
from models.scenes.scenes_base import Scene
from models.world.world import get_location
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen


class BackgroundArtist(SceneArtist):
    """Draws the background image."""

    def render(self, screen: Screen, scene: Scene, layout: Layout) -> None:
        background_image = get_location().background_image_path
        w, h = SCREEN_SIZE
        screen.render_image(background_image, 0, 0, w, h)
