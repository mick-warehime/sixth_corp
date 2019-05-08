from typing import List

from data.colors import GREEN
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene
from views.artists.background_artist import BackgroundArtist
from views.artists.combat_artist import CombatArtist
from views.artists.decision_artist import DecisionArtist
from views.artists.inventory_artist import InventoryArtist
from views.artists.overlay_artist import OverlayArtist
from views.artists.scene_artist_base import SceneArtist
from views.artists.settings_artist import SettingsArtist
from views.pygame_screen import get_screen


class SceneView(object):
    """Manages all drawing on the screen for a given scene."""

    def __init__(self, scene: Scene) -> None:
        self._scene = scene
        self._screen = get_screen()
        self._artists = _build_scene_artists(scene)
        self._debug_mode = False

    def update(self) -> None:
        self._screen.clear()
        for artist in self._artists:
            artist.render(self._screen, self._scene)
        if self._debug_mode and hasattr(self._scene, 'layout'):
            layout = self._scene.layout  # type: ignore
            for rect in layout.get_rects(layout):
                self._screen.render_rect(rect, GREEN, 2)

        # VERY IMPORTANT TO CALL UPDATE ONCE
        self._screen.update()

    def toggle_debug(self) -> None:
        """Toggle DEBUG mode, where all layout rects are drawn."""
        self._debug_mode = not self._debug_mode


def _build_scene_artists(scene: Scene) -> List[SceneArtist]:
    if isinstance(scene, CombatScene):
        artists = [BackgroundArtist(scene), OverlayArtist(), CombatArtist()]
    elif isinstance(scene, DecisionScene):
        artists = [BackgroundArtist(scene), OverlayArtist(), DecisionArtist()]
    elif isinstance(scene, SettingsScene):
        artists = [BackgroundArtist(scene), OverlayArtist(), SettingsArtist()]
    elif isinstance(scene, InventoryScene):
        artists = [BackgroundArtist(scene), InventoryArtist()]
    else:
        raise ValueError('Unrecognized Scene {}'.format(scene))
    return artists
