from data.colors import WHITE
from scenes.settings_scene import SettingsScene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen


class SettingsArtist(SceneArtist):

    def render(self, screen: Screen, scene: SettingsScene) -> None:
        background_image = scene.background

        x, font_size, spacing = rescale_horizontal(250, 35, 50)
        y = rescale_vertical(250)
        screen.render_image(background_image, x=0, y=0, h=0, w=0)
        screen.render_texts(
            list(scene.options),
            font_size=font_size,
            x=x,
            y=y,
            color=WHITE,
            spacing=spacing)
