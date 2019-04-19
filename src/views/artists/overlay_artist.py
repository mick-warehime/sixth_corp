from data.colors import WHITE
from models.scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class OverlayArtist(SceneArtist):
    """Draws basic overlay information, like player health."""

    def render(self, screen: Screen, scene: Scene) -> None:

        # key hints
        screen.render_text('i: Inventory', 28, 20, 50, WHITE)
        screen.render_text('d: debug', 28, 20, 75, WHITE)
        screen.render_text('x: Settings', 28, 1050, 15, WHITE)
