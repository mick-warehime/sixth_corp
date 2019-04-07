from pygame.rect import Rect

from characters.player import get_player
from models.characters.states import Attributes
from data import constants
from data.colors import DARK_GRAY, RED, WHITE
from scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen
from world.world import get_location


class OverlayArtist(SceneArtist):
    """Draws basic overlay information, like player health."""

    def render(self, screen: Screen, scene: Scene, layout: Layout) -> None:
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

        # draw scene number
        scene_text = 'Scene: {}'.format(get_location().scene_number)
        x_scene = int(width / 2 + 100)
        y_scene = int(height / 2 - 5)
        screen.render_text(scene_text, 22, x_scene, y_scene, WHITE)

        # key hints
        screen.render_text('i: Inventory', 28, 20, 50, WHITE)
        screen.render_text('d: debug', 28, 20, 75, WHITE)
        screen.render_text('x: Settings', 28, 1050, 15, WHITE)
