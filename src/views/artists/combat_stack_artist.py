from data.colors import DARK_GRAY, LIGHT_GRAY, RED, WHITE
from models.characters.subroutine_examples import FireLaser, Repair
from models.combat.moves_base import Move
from models.scenes.combat_scene import CombatScene
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen
from views.stack_utils import stack_rect

_TEXT_SPACE, = rescale_horizontal(10)
_STACK_OUTLINE, = rescale_horizontal(2)
_FONT_SIZE, = rescale_horizontal(24)
_TARGET_SIZE, = rescale_horizontal(50)


class CombatStackArtist(SceneArtist):

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)
        player, enemy = scene.characters()
        stack = [
            Move(FireLaser(2), player, enemy),
            Move(FireLaser(1), enemy, player), Move(Repair(1), player, player)]
        for i, move in enumerate(stack):
            rect = stack_rect(i)

            # Stack Ability + timer
            fake_time = len(stack) - i
            screen.render_rect(rect, DARK_GRAY, 0)
            screen.render_rect(rect, LIGHT_GRAY, _STACK_OUTLINE)
            screen.render_text(
                move.subroutine.description(),
                _FONT_SIZE,
                rect.x + _TEXT_SPACE,
                rect.y + _TEXT_SPACE,
                WHITE)
            screen.render_text(
                'T: {}'.format(fake_time),
                _FONT_SIZE,
                rect.x + rect.w - 5 * _TEXT_SPACE,
                rect.y + _TEXT_SPACE, RED)

            # USER + TARGET
            screen.render_image(
                move.user.image_path,
                rect.x - _TARGET_SIZE,
                rect.y,
                _TARGET_SIZE,
                _TARGET_SIZE)
            screen.render_image(
                move.target.image_path,
                rect.x + rect.w,
                rect.y,
                _TARGET_SIZE,
                _TARGET_SIZE)
