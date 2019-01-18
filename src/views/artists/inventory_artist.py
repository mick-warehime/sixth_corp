from data.colors import WHITE
from scenes.inventory_scene import InventoryScene
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: InventoryScene) -> None:
        background_image = scene.background
        screen.render_image(background_image, x=0, y=0, h=0, w=0)
        screen.render_texts(
            list(
                scene.options),
            font_size=35,
            x=250,
            y=250,
            color=WHITE,
            spacing=50)
