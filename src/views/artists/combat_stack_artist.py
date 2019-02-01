from characters.player import get_player
from characters.subroutine_examples import FireLaser, Repair
from combat.moves_factory import build_move
from data.colors import DARK_GRAY, LIGHT_GRAY, RED, WHITE
from scenes.combat_scene import CombatScene
from views.artists.drawing_utils import rescale_horizontal
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen
from views.stack_utils import stack_position

_TEXT_SPACE, = rescale_horizontal(10)
_STACK_OUTLINE, = rescale_horizontal(2)
_FONT_SIZE, = rescale_horizontal(24)
_TARGET_SIZE, = rescale_horizontal(50)


class CombatStackArtist(SceneArtist):

    def render(self, screen: Screen, scene: CombatScene) -> None:
        player = get_player()
        enemy = scene.enemy()
        stack = [
            build_move(
                FireLaser(2), player, enemy), build_move(
                FireLaser(1), enemy, player), build_move(
                Repair(1), player, player)]
        for i, move in enumerate(stack):
            pos = stack_position(i)

            # Stack Ability + timer
            fake_time = len(stack) - i
            screen.render_rect(pos.x, pos.y, pos.w, pos.h, DARK_GRAY, 0)
            screen.render_rect(pos.x, pos.y, pos.w, pos.h, LIGHT_GRAY,
                               _STACK_OUTLINE)
            screen.render_text(
                move.subroutine.description(),
                _FONT_SIZE,
                pos.x + _TEXT_SPACE,
                pos.y + _TEXT_SPACE,
                WHITE)
            screen.render_text(
                'T: {}'.format(fake_time),
                _FONT_SIZE,
                pos.x + pos.w - 5 * _TEXT_SPACE,
                pos.y + _TEXT_SPACE, RED)

            # USER + TARGET
            screen.render_image(
                move.user.image_path,
                pos.x - _TARGET_SIZE,
                pos.y,
                _TARGET_SIZE,
                _TARGET_SIZE)
            screen.render_image(
                move.target.image_path,
                pos.x + pos.w,
                pos.y,
                _TARGET_SIZE,
                _TARGET_SIZE)
