from data.colors import WHITE
from data.constants import SCREEN_SIZE
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import Scene
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class InventoryArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, InventoryScene)

        screen.render_texts(list(scene.options),
                            font_size=35,
                            x=250,
                            y=250,
                            color=WHITE,
                            spacing=50)
