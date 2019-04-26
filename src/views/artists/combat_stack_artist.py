import logging
from typing import Dict, List, Optional, Tuple

from pygame.rect import Rect

from data.colors import DARK_GRAY, LIGHT_GRAY, RED, WHITE, YELLOW
from models.combat.moves_base import Move
from models.scenes.combat_scene import CombatScene, MoveData
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_TEXT_SPACE, = rescale_horizontal(10)
_STACK_OUTLINE, = rescale_horizontal(2)
_FONT_SIZE, = rescale_horizontal(24)
_TARGET_SIZE, = rescale_horizontal(50)
_SMALL_FONT_SIZE, = rescale_horizontal(18)


def _render_move(move: Move, time: Optional[int], rect: Rect,
                 screen: Screen, small_text: bool = False,
                 CPU_not_time: bool = False) -> None:
    # Background
    screen.render_rect(rect, DARK_GRAY, 0)
    screen.render_rect(rect, LIGHT_GRAY, _STACK_OUTLINE)

    font_size = _SMALL_FONT_SIZE if small_text else _FONT_SIZE
    # Description
    screen.render_text(
        move.subroutine.description(),
        font_size,
        rect.x + _TEXT_SPACE,
        rect.y + _TEXT_SPACE,
        WHITE)

    # CPU slots
    if CPU_not_time:
        screen.render_text(
            'CPU: {}'.format(move.subroutine.cpu_slots()),
            font_size,
            rect.x + rect.w - 6 * _TEXT_SPACE,
            rect.y + _TEXT_SPACE, YELLOW)
    # Time to resolve
    elif time is not None:
        screen.render_text(
            'T: {}'.format(time),
            font_size,
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


def _interpolate(progress: float, rect_prev: Rect,
                 rect_new: Rect) -> Rect:
    # Interpolate parameters between two rects
    assert 0 <= progress <= 1.0
    x = rect_prev.x + (rect_new.x - rect_prev.x) * progress
    y = rect_prev.y + (rect_new.y - rect_prev.y) * progress
    w = rect_prev.w + (rect_new.w - rect_prev.w) * progress
    h = rect_prev.h + (rect_new.h - rect_prev.h) * progress
    return Rect(x, y, w, h)


class CombatStackArtist(SceneArtist):

    def __init__(self) -> None:
        self._prev_move_data_rects: Dict[MoveData, List[Rect]] = {}
        self._move_data_rects: Dict[MoveData, List[Rect]] = {}
        self._first_animation = True

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)

        current_move_datas = [data for data in scene.layout.all_objects()
                              if isinstance(data, MoveData)]

        # Each element of this is passed to the render function.
        stack_render_data: List[Tuple[MoveData, List[Rect]]] = []

        # Beginning of animation
        # As soon as moves are selected, the scene layout is instantly updated
        # to match the end of the animation. In order to animate we must keep
        # track of both the current layout and the previous layout. During the
        # animation the rects from the previous layout are matched with rects
        # in the new layout to get an interpolated rect that is used in
        # rendering.
        if scene.animation_progress is not None and self._first_animation:
            logging.debug('Animation start')
            self._first_animation = False
            # data and relevant rects for the new layout. We only consider moves
            # that existed in the previous round. The time_left in the current
            # round is thus decremented by one.
            self._move_data_rects = {
                data: scene.layout.get_rects(data.time_minus_one())
                for data in self._prev_move_data_rects}
            # Also include the moves that have just resolved.
            self._move_data_rects.update(
                {data: scene.layout.get_rects(data)
                 for data in current_move_datas if data.time_left == 0})
            stack_render_data = list(self._prev_move_data_rects.items())
            show_resolved = False

        # Middle of animation. Do not animate the first animation as there is
        # nothing to draw.
        elif scene.animation_progress is not None and not self._first_animation:
            # interpolate prev and new rects based on animation progress
            for data, prev_rects in self._prev_move_data_rects.items():
                new_rects = self._move_data_rects[data]

                assert len(prev_rects) == len(new_rects)

                interp_rects = [_interpolate(scene.animation_progress, *old_new)
                                for old_new in zip(prev_rects, new_rects)]
                stack_render_data.append((data, interp_rects))  # type: ignore

            show_resolved = False

        # No animation, show resolved moves and current layout.
        else:
            assert scene.animation_progress is None
            self._first_animation = True

            self._prev_move_data_rects = {data: scene.layout.get_rects(data)
                                          for data in current_move_datas
                                          if data.time_left
                                          and not data.under_char}

            stack_render_data = list(self._prev_move_data_rects.items())
            show_resolved = True

        # Render moves on the stack (not yet resolved)
        for data, rects in stack_render_data:
            for rect in rects:
                _render_move(data.move, data.time_left, rect, screen)

        # Render resolved moves
        if show_resolved:
            for data in current_move_datas:
                if data.time_left:
                    continue
                for rect in scene.layout.get_rects(data):
                    _render_move(data.move, None, rect, screen)

        # Render moves under characters
        for data in current_move_datas:
            if not data.under_char:
                continue
            rects = scene.layout.get_rects(data)
            assert len(rects) == 1
            _render_move(data.move, None, rects[0], screen,
                         small_text=True, CPU_not_time=True)
