from functools import reduce
from typing import List

from data.colors import GREEN
from data.constants import SCREEN_SIZE
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene
from views.artists.background_artist import BackgroundArtist
from views.artists.character_artist import CharacterArtist
from views.artists.combat_options_artist import CombatOptionsArtist
from views.artists.combat_stack_artist import CombatStackArtist
from views.artists.decision_artist import DecisionArtist
from views.artists.inventory_artist import InventoryArtist
from views.artists.overlay_artist import OverlayArtist
from views.artists.scene_artist_base import SceneArtist
from views.artists.settings_artist import SettingsArtist
from views.layouts import Layout
from views.pygame_screen import get_screen


class SceneView(object):

    def __init__(self, scene: Scene) -> None:
        self._scene = scene
        self._screen = get_screen()
        self._artists = _build_scene_artists(scene)
        self._layout = _build_scene_layout(scene)
        self._debug_mode = False

    def update(self) -> None:
        self._screen.clear()
        for artist in self._artists:
            artist.render(self._screen, self._scene, self._layout)
        # VERY IMPORTANT TO CALL UPDATE ONCE
        if self._debug_mode:
            for rect in self._layout.get_rects(self._layout):
                self._screen.render_rect(rect, GREEN, 2)
        self._screen.update()

    @property
    def layout(self) -> Layout:
        return self._layout

    def toggle_debug(self) -> None:
        """Toggle DEBUG mode, where all layout rects are drawn."""
        self._debug_mode = not self._debug_mode


def _build_scene_artists(scene: Scene) -> List[SceneArtist]:
    if isinstance(scene, CombatScene):
        artists = [BackgroundArtist(scene), OverlayArtist(),
                   CharacterArtist(), CombatOptionsArtist(),
                   CombatStackArtist()]
    elif isinstance(scene, DecisionScene):
        artists = [BackgroundArtist(scene), DecisionArtist()]
    elif isinstance(scene, SettingsScene):
        artists = [BackgroundArtist(scene), SettingsArtist()]
    elif isinstance(scene, InventoryScene):
        artists = [BackgroundArtist(scene), InventoryArtist()]
    else:
        raise ValueError('Unrecognized Scene {}'.format(scene))
    return artists


def _build_scene_layout(scene: Scene) -> Layout:
    if isinstance(scene, CombatScene):
        characters = scene.characters()
        # player side layout
        player = characters[0]

        player_layout = Layout([(None, 2), (player, 1), (None, 2)], 'vertical')
        player_layout = Layout([(None, 1), (player_layout, 1), (None, 1)],
                               'horizontal')

        # stack layout
        stack_layout = Layout()

        # enemies layout
        assert len(characters) > 1
        elements = reduce(lambda a, b: a + b,
                          ([(None, 1), (e, 1)] for e in characters[1:]))
        elements.append((None, 1))
        enemies_layout = Layout(elements, 'vertical')

        return Layout(
            [(player_layout, 1), (stack_layout, 1), (enemies_layout, 1)],
            'horizontal', SCREEN_SIZE)

    return Layout(dimensions=SCREEN_SIZE)
