from data.colors import WHITE
from data.constants import SCREEN_SIZE
from scenes.inventory_scene import InventoryScene
from scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene,
               layout: Layout) -> None:
        assert isinstance(scene, InventoryScene)
        background_image = scene.background

        screen.render_image(background_image, 0, 0, *SCREEN_SIZE)
        screen.render_texts(list(scene.options),
                            font_size=35,
                            x=250,
                            y=250,
                            color=WHITE,
                            spacing=50)
