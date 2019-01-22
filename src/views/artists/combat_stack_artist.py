from characters.player import get_player
from characters.subroutine_examples import FireLaser, Repair
from combat.moves_factory import build_move
from data.colors import DARK_GRAY, LIGHT_GRAY, RED, WHITE
from scenes.combat_scene import CombatScene
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen

_STACK_TOP_X = 425
_STACK_TOP_Y = 200
_STACK_WIDTH = 250
_STACK_HEIGHT = 50
_STACK_OUTLINE = 2
_TEXT_DELTA_X = 10
_TEXT_DELTA_Y = 10
_FONT_SIZE = 24
_TARGET_SIZE = 50


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
            x = _STACK_TOP_X
            y = _STACK_TOP_Y + i * _STACK_HEIGHT

            # Stack Ability + timer
            fake_time = len(stack) - i
            screen.render_rect(x, y, _STACK_WIDTH, _STACK_HEIGHT, DARK_GRAY, 0)
            screen.render_rect(x, y, _STACK_WIDTH, _STACK_HEIGHT, LIGHT_GRAY, _STACK_OUTLINE)
            screen.render_text(
                move.subroutine.description(),
                _FONT_SIZE,
                x + _TEXT_DELTA_X,
                y + _TEXT_DELTA_Y,
                WHITE)
            screen.render_text(
                'T: {}'.format(fake_time),
                _FONT_SIZE,
                x +
                _STACK_WIDTH -
                5 *
                _TEXT_DELTA_X,
                y +
                _TEXT_DELTA_Y,
                RED)

            # USER + TARGET
            screen.render_image(
                move.user.image_path,
                x - _TARGET_SIZE,
                y,
                _TARGET_SIZE,
                _TARGET_SIZE)
            screen.render_image(
                move.target.image_path,
                x + _STACK_WIDTH,
                y,
                _TARGET_SIZE,
                _TARGET_SIZE)
