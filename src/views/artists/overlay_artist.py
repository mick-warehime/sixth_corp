from pygame.rect import Rect

from data import constants
from data.colors import DARK_GRAY, RED, WHITE
from models.characters.player import get_player
from models.characters.states import Attributes
from models.scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class OverlayArtist(SceneArtist):
    """Draws basic overlay information, like player health."""

    def render(self, screen: Screen, scene: Scene) -> None:
        # draw gray background
        height = 40
        width = constants.SCREEN_SIZE[0]
        screen.render_rect(Rect(0, 0, width, height), DARK_GRAY, 0)

        # draw health
        player = get_player()
        health = player.status.get_attribute(Attributes.HEALTH)
        max_health = player.status.get_attribute(Attributes.MAX_HEALTH)
        health_text = 'Health: {} / {}'.format(health, max_health)
        x_health = int(width / 2 - 300)
        y_health = int(height / 2 - 5)
        screen.render_text(health_text, font_size=21, x=x_health, y=y_health,
                           color=RED)

        # key hints
        screen.render_text('i: Inventory', 28, 20, 50, WHITE)
        screen.render_text('d: debug', 28, 20, 75, WHITE)
        screen.render_text('x: Settings', 28, 1050, 15, WHITE)
