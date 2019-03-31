from data.colors import WHITE
from data.constants import SCREEN_SIZE
from scenes.settings_scene import SettingsScene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.screen_base import Screen


class SettingsArtist(SceneArtist):

    def render(self, screen: Screen, scene: SettingsScene,
               layout: Layout) -> None:
        background_image = scene.background

        x, font_size, spacing = rescale_horizontal(250, 35, 50)
        y, = rescale_vertical(250)
        screen.render_image(background_image, 0, 0, *SCREEN_SIZE)
        screen.render_texts(
            list(scene.options),
            font_size=font_size,
            x=x,
            y=y,
            color=WHITE,
            spacing=spacing)
