from typing import Sequence

from combat.moves_base import Move
from data.colors import GREEN
from scenes.combat_scene import CombatScene
from views.scene_artist_base import SceneArtist
from views.screen_base import Screen


class CombatOptionsArtist(SceneArtist):

    def render(self, screen: Screen, scene: CombatScene) -> None:
        options = self._combat_options(scene.current_moves)
        screen.render_texts(options, font_size=25, x=200, y=200, color=GREEN)

    def _combat_options(self, moves: Sequence[Move]) -> Sequence[str]:
        return ['{} - {}'.format(i + 1, m.ability.description())
                for i, m in enumerate(moves)]
