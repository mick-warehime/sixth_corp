import logging
from typing import Dict, List, Tuple, Optional

from pygame.rect import Rect

from data.colors import DARK_GRAY, LIGHT_GRAY, RED, WHITE
from models.combat.moves_base import Move
from models.scenes.combat_scene import CombatScene
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen

_TEXT_SPACE, = rescale_horizontal(10)
_STACK_OUTLINE, = rescale_horizontal(2)
_FONT_SIZE, = rescale_horizontal(24)
_TARGET_SIZE, = rescale_horizontal(50)


def _render_move(move: Move, time: Optional[int], rect: Rect,
                 screen: Screen) -> None:
    # Stack Ability + timer
    screen.render_rect(rect, DARK_GRAY, 0)
    screen.render_rect(rect, LIGHT_GRAY, _STACK_OUTLINE)
    screen.render_text(
        move.subroutine.description(),
        _FONT_SIZE,
        rect.x + _TEXT_SPACE,
        rect.y + _TEXT_SPACE,
        WHITE)
    if time is not None:
        screen.render_text(
            'T: {}'.format(time),
            _FONT_SIZE,
            rect.x + rect.w - 7 * _TEXT_SPACE,
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

    def __init__(self):
        self._prev_move_rects: Dict[Tuple[Move, int], List[Rect]] = {}
        self._new_move_rects: Dict[Tuple[Move, int], List[Rect]] = {}
        self._animation_start = True

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)

        move_time_rects: List[Tuple[Move, int, List[Rect]]] = []

        # Beginning of animation
        if scene.animation_progress is not None and self._animation_start:
            logging.debug('Animation start')
            self._animation_start = False
            self._new_move_rects = {
                m_t: scene.layout.get_rects((m_t[0], m_t[1] - 1))
                for m_t in self._prev_move_rects}
            resolved = scene.combat_stack.extract_resolved_moves()
            self._new_move_rects.update({(m, 1): scene.layout.get_rects(m)
                                         for m in resolved})
            move_time_rects = list(m_t + (rects,) for m_t, rects in
                                   self._prev_move_rects.items())
            show_resolved = False

        # Middle of animation
        elif scene.animation_progress is not None and not self._animation_start:
            # interpolate prev and new rects based on animation progress

            for m_t, prev_rects in self._prev_move_rects.items():
                new_rects = self._new_move_rects[m_t]

                assert len(prev_rects) == len(new_rects)

                interp_rects = [_interpolate(scene.animation_progress, *p_n)
                                for p_n in zip(prev_rects, new_rects)]
                move_time_rects.append(m_t + (interp_rects,))

            show_resolved = False

        # No animation
        else:
            assert scene.animation_progress is None
            self._animation_start = True

            self._prev_move_rects = {m_t: scene.layout.get_rects(m_t)
                                     for m_t in
                                     scene.combat_stack.moves_times_remaining()}
            move_time_rects = list(m_t + (rects,) for m_t, rects in
                                   self._prev_move_rects.items())
            show_resolved = True

        for move, time, rects in move_time_rects:
            for rect in rects:
                _render_move(move, time, rect, screen)

        if show_resolved:
            for move in scene.combat_stack.extract_resolved_moves():
                rects = scene.layout.get_rects(move)

                for rect in rects:
                    _render_move(move, None, rect, screen)
