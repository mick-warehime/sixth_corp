from data.colors import WHITE
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class SettingsArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, SettingsScene)

        x, font_size, spacing = rescale_horizontal(250, 35, 50)
        y, = rescale_vertical(250)
        screen.render_texts(list(scene.options),
                            font_size=font_size,
                            x=x,
                            y=y,
                            color=WHITE,
                            spacing=spacing)
