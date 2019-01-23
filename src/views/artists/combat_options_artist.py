from typing import Sequence

from combat.moves_base import Move
from data.colors import GREEN
from scenes.combat_scene import CombatScene
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen


class CombatOptionsArtist(SceneArtist):

    def render(self, screen: Screen, scene: CombatScene) -> None:
        options = self._combat_options(scene.current_moves)
        screen.render_texts(list(options), font_size=25, x=450, y=700, color=GREEN, spacing=50)

    def _combat_options(self, moves: Sequence[Move]) -> Sequence[str]:
        return ['{} - {}'.format(i + 1, m.subroutine.description())
                for i, m in enumerate(moves)]
