from functools import reduce
from typing import List

from data.constants import SCREEN_SIZE
from views.layouts import Layout
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
from views.artists.inventory_artist import InventoryArtist
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
        self._layout = _build_scene_layout(scene)

    def update(self) -> None:
        self._screen.clear()
        for artist in self._artists:
            artist.render(screen=self._screen, scene=self._scene)
        # VERY IMPORTANT TO CALL UPDATE ONCE
        self._screen.update()

    @property
    def layout(self) -> Layout:
        return self._layout


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
        artists = [InventoryArtist()]
    else:
        raise ValueError('Unrecognized Scene {}'.format(scene))
    return artists


def _build_scene_layout(scene) -> Layout:
    if isinstance(scene, CombatScene):
        characters = scene.characters()
        # player side layout
        player = characters[0]
        player_layout = Layout([(None, 1), (player, 1), (None, 1)], 'vertical')

        # stack layout
        stack_layout = Layout()

        # enemies layout
        elements = [[(e, 1), (None, 1)] for e in characters[1:]]
        elements = reduce(lambda a, b: a + b, elements)
        enemies_layout = Layout(elements, 'vertical')

        return Layout(
            [(player_layout, 1), (stack_layout, 1), (enemies_layout, 1)],
            'horizontal', SCREEN_SIZE)

    return Layout(dimensions=SCREEN_SIZE)
