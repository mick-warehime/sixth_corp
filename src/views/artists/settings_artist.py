from data.colors import WHITE
from scenes.settings_scene import SettingsScene
from views.scene_artist_base import SceneArtist
from views.screen_base import Screen


class SettingsArtist(SceneArtist):

    def render(self, screen: Screen, scene: SettingsScene) -> None:
        background_image = scene.background
        screen.render_image(background_image, 0, 0)
        screen.render_texts(scene.options, font_size=35, x=250, y=250, color=WHITE)
