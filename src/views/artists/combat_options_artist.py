from typing import Sequence

from combat.moves_base import Move
from data.colors import GREEN
from scenes.combat_scene import CombatScene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.screen_base import Screen


class CombatOptionsArtist(SceneArtist):

    def render(self, screen: Screen, scene: CombatScene,
               layout: Layout) -> None:
        options = self._combat_options(scene.current_moves)
        x, font_size, spacing = rescale_horizontal(450, 35, 50)
        y, = rescale_vertical(700)
        screen.render_texts(list(options), font_size=font_size, x=x, y=y,
                            color=GREEN, spacing=spacing)

    def _combat_options(self, moves: Sequence[Move]) -> Sequence[str]:
        return ['{} - {}'.format(i + 1, m.subroutine.description())
                for i, m in enumerate(moves)]
