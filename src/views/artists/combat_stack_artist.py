from data.colors import DARK_GRAY, LIGHT_GRAY, RED, WHITE
from scenes.combat_scene import CombatScene
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen
from views.stack_utils import stack_position

_TEXT_SPACE = 10
_STACK_OUTLINE = 2
_FONT_SIZE = 24
_TARGET_SIZE = 50


class CombatStackArtist(SceneArtist):

    def render(self, screen: Screen, scene: CombatScene) -> None:
        for i, move in enumerate(scene.stack):
            pos = stack_position(i)

            # Stack Ability + timer
            fake_time = len(scene.stack) - i
            screen.render_rect(pos.x, pos.y, pos.w, pos.h, DARK_GRAY, 0)
            screen.render_rect(pos.x, pos.y, pos.w, pos.h, LIGHT_GRAY, _STACK_OUTLINE)
            screen.render_text(
                move.subroutine.description(),
                _FONT_SIZE,
                pos.x + _TEXT_SPACE,
                pos.y + _TEXT_SPACE,
                WHITE)
            screen.render_text(
                'T: {}'.format(fake_time),
                _FONT_SIZE,
                pos.x +
                pos.w -
                5 *
                _TEXT_SPACE,
                pos.y +
                _TEXT_SPACE,
                RED)

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
