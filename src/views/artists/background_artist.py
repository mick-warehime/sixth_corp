from data.constants import SCREEN_SIZE
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen

_background_image = 'src/data/images/background_loading.png'
_BACKGROUND_IMAGE_LOADING = 'src/data/images/background_loading.png'
_BACKGROUND_IMAGE_CITY = 'src/data/images/background_city.png'
_BACKGROUND_IMAGE_MARS = 'src/data/images/background_mars.png'
_BACKGROUND_SETTINGS = 'src/data/images/background_settings.png'
_BACKGROUND_INVENTORY = 'src/data/images/background_inventory.png'


class BackgroundArtist(SceneArtist):
    """Draws the background image."""

    def __init__(self, scene: Scene):
        self._background_image: str = _BACKGROUND_IMAGE_LOADING
        if isinstance(scene, (CombatScene, DecisionScene)):
            self._background_image = _BACKGROUND_IMAGE_CITY
        elif isinstance(scene, SettingsScene):
            self._background_image = _BACKGROUND_SETTINGS
        elif isinstance(scene, InventoryScene):
            self._background_image = _BACKGROUND_INVENTORY

    def render(self, screen: Screen, scene: Scene, layout: Layout) -> None:
        w, h = SCREEN_SIZE
        screen.render_image(self._background_image, 0, 0, w, h)
