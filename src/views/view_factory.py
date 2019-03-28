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
from views.artists.settings_artist import SettingsArtist
from views.scene_view import SceneView
from views.view_base import View


def build_scene_view(scene: Scene) -> View:
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
    return SceneView(scene, artists)
