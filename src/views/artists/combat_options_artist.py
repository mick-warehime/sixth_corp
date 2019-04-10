from typing import Sequence

from data.colors import GREEN
from models.combat.moves_base import Move
from models.scenes.combat_scene import CombatScene
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class CombatOptionsArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)
        options = self._combat_options(scene.current_moves)
        x, font_size, spacing = rescale_horizontal(450, 35, 50)
        y, = rescale_vertical(700)
        screen.render_texts(list(options), font_size=font_size, x=x, y=y,
                            color=GREEN, spacing=spacing)

    def _combat_options(self, moves: Sequence[Move]) -> Sequence[str]:
        return ['{} - {}'.format(i + 1, m.subroutine.description())
                for i, m in enumerate(moves)]
