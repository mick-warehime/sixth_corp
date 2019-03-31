from data.colors import WHITE
from data.constants import SCREEN_SIZE
from scenes.inventory_scene import InventoryScene
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.screen_base import Screen


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: InventoryScene,
               layout: Layout) -> None:
        background_image = scene.background

        screen.render_image(background_image, 0, 0, *SCREEN_SIZE)
        screen.render_texts(list(scene.options),
                            font_size=35,
                            x=250,
                            y=250,
                            color=WHITE,
                            spacing=50)
