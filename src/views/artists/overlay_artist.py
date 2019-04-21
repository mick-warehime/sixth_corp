from data.colors import WHITE
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_FONT_SIZE, = rescale_horizontal(28)


class OverlayArtist(SceneArtist):
    """Draws basic overlay information, like player health."""

    def render(self, screen: Screen, scene: Scene) -> None:

        # key hints
        x = 20
        y = 10
        line_spacing = 10

        rect = screen.render_text('x: Settings', _FONT_SIZE, x, y, WHITE)
        y += rect.h + line_spacing

        if hasattr(scene, 'inventory_available'):
            if scene.inventory_available:  # type: ignore
                rect = screen.render_text('i: Inventory', _FONT_SIZE, x, y,
                                          WHITE)
                y += rect.h + line_spacing

        if hasattr(scene, 'layout'):
            screen.render_text('d: debug', _FONT_SIZE, x, y, WHITE)
