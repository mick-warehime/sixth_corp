from enum import Enum

from scenes.scenes_base import Scene
from views.artists.background_artist import BackgroundArtist
from views.artists.character_artist import CharacterArtist
from views.artists.combat_options_artist import CombatOptionsArtist
from views.artists.decision_artist import DecisionArtist
from views.artists.overlay_artist import OverlayArtist
from views.artists.settings_artist import SettingsArtist
from views.scene_view import SceneView
from views.view_base import View


class SceneViewType(Enum):
    Combat = 'combat'
    Decision = 'decision'
    Settings = 'settings'
    Inventory = 'inventory'


def build_scene_view(view_type: SceneViewType, scene: Scene) -> View:
    if view_type == SceneViewType.Combat:
        artists = [BackgroundArtist(), OverlayArtist(), CharacterArtist(), CombatOptionsArtist()]
    elif view_type == SceneViewType.Decision:
        artists = [BackgroundArtist(), DecisionArtist()]
    elif view_type == SceneViewType.Settings:
        artists = [SettingsArtist()]
    elif view_type == SceneViewType.Inventory:
        artists = [SettingsArtist()]
    else:
        raise ValueError('No such view type: {}'.format(view_type))
    return SceneView(scene, artists)
