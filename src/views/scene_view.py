from typing import List

from scenes.combat_scene import CombatScene
from scenes.decision_scene import DecisionScene
from scenes.inventory_scene import InventoryScene
from scenes.scenes_base import Scene
from scenes.settings_scene import SettingsScene
from views.artists.background_artist import BackgroundArtist
from views.artists.character_artist import CharacterArtist
from views.artists.combat_options_artist import CombatOptionsArtist
from views.artists.combat_stack_artist import CombatStackArtist
from views.artists.decision_artist import DecisionArtist
from views.artists.overlay_artist import OverlayArtist
from views.artists.scene_artist_base import SceneArtist
from views.artists.settings_artist import SettingsArtist
from views.screen_factory import get_screen
from views.view_base import View


class SceneView(View):

    def __init__(self, scene: Scene) -> None:
        self._scene = scene
        self._screen = get_screen()
        self._artists = _build_scene_artists(scene)

    def update(self) -> None:
        self._screen.clear()
        for artist in self._artists:
            artist.render(screen=self._screen, scene=self._scene)
        # VERY IMPORTANT TO CALL UPDATE ONCE
        self._screen.update()


def _build_scene_artists(scene: Scene) -> List[SceneArtist]:
    if isinstance(scene, CombatScene):
        artists = [
            BackgroundArtist(),
            OverlayArtist(),
            CharacterArtist(),
            CombatOptionsArtist(),
            CombatStackArtist()]
    elif isinstance(scene, DecisionScene):
        artists = [BackgroundArtist(), DecisionArtist()]
    elif isinstance(scene, SettingsScene):
        artists = [SettingsArtist()]
    elif isinstance(scene, InventoryScene):
        artists = [SettingsArtist()]
    else:
        raise ValueError('Unrecognized Scene {}'.format(scene))
    return artists
