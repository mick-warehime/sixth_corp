from characters.player import get_player
from characters.states import Attribute
from data import constants
from data.colors import DARK_GRAY, RED, WHITE
from scenes.scenes_base import Scene
from views.scene_artist_base import SceneArtist
from views.screen_base import Screen
from world.world import get_location


class OverlayArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        # draw gray background
        height = 40
        width = constants.SCREEN_SIZE[0]
        screen.render_rect(0, 0, width, height, DARK_GRAY)

        # draw health
        player = get_player()
        health = player.get_attribute(Attribute.HEALTH)
        max_health = player.get_attribute(Attribute.MAX_HEALTH)
        health_text = 'Health: {} / {}'.format(health, max_health)
        x_health = int(width / 2 - 300)
        y_health = int(height / 2 - 5)
        screen.render_text(health_text, 21, x_health, y_health, RED)

        # draw scene number
        scene_text = 'Scene: {}'.format(get_location().scene)
        x_scene = int(width / 2 + 100)
        y_scene = int(height / 2 - 5)
        screen.render_text(scene_text, 22, x_scene, y_scene, WHITE)
