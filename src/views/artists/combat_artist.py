import logging
from typing import Dict, List, Optional

from pygame.rect import Rect

from data.colors import (DARK_GRAY, GREEN, LIGHT_BLUE, LIGHT_GRAY, RED, WHITE,
                         YELLOW)
from models.characters.moves_base import Move
from models.scenes.combat_scene import CharacterInfo, CombatScene, MoveInfo
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
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


def _render_characters(scene: CombatScene, screen: Screen) -> None:
    char_infos = [data for data in scene.layout.all_objects()
                  if isinstance(data, CharacterInfo)]

    for info in char_infos:
        rects = scene.layout.get_rects(info)
        assert len(rects) == 1

        rect = rects[0]
        _render_character(info, screen, rect)


class CombatArtist(SceneArtist):

    def __init__(self) -> None:
        self._prev_move_data_rects: Dict[MoveInfo, List[Rect]] = {}
        self._move_data_rects: Dict[MoveInfo, List[Rect]] = {}
        self._animation_start = True

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)

        _render_characters(scene, screen)

        self._render_moves(scene, screen)

        _render_combat_options(scene, screen)

    def _render_moves(self, scene: CombatScene, screen: Screen) -> None:
        current_move_datas = [data for data in scene.layout.all_objects()
                              if isinstance(data, MoveInfo)]
        # Each key_value pair is passed to the render function.
        stack_render_data: Dict[MoveInfo, List[Rect]] = {}
        # Beginning of animation
        # As soon as moves are selected, the scene layout is instantly updated
        # to match the end of the animation. In order to animate we must keep
        # track of both the current layout and the previous layout. During the
        # animation the rects from the previous layout are matched with rects
        # in the new layout to get an interpolated rect that is used in
        # rendering.
        if scene.animation_progress is not None and self._animation_start:
            logging.debug('Animation start')
            self._animation_start = False
            # We only consider moves that existed in the previous round,
            # excluding those that resolved.
            to_remove = [data for data in self._prev_move_data_rects
                         if not data.time_left]
            for move_data in to_remove:
                self._prev_move_data_rects.pop(move_data)

            # Match data and relevant rects for the new layout. The time_left
            # in the current round is thus decremented by one.
            self._move_data_rects = {
                data: scene.layout.get_rects(data.time_minus_one())
                for data in self._prev_move_data_rects}

            # Also include the moves that have just resolved (which may not
            # have existed in the last round).
            self._move_data_rects.update(
                {data: scene.layout.get_rects(data)
                 for data in current_move_datas if data.time_left == 0})

            stack_render_data = self._prev_move_data_rects

        # Middle of animation.
        elif scene.animation_progress is not None and not self._animation_start:
            # interpolate prev and new rects based on animation progress
            for data, prev_rects in self._prev_move_data_rects.items():
                new_rects = self._move_data_rects[data]

                assert len(prev_rects) == len(new_rects), '{}'.format(data)

                interp_rects = [_interpolate(scene.animation_progress, *old_new)
                                for old_new in zip(prev_rects, new_rects)]
                stack_render_data[data] = interp_rects

        # No animation, show resolved moves and current layout.
        else:
            assert scene.animation_progress is None
            self._animation_start = True

            self._prev_move_data_rects = {data: scene.layout.get_rects(data)
                                          for data in current_move_datas
                                          if not data.under_char}

            stack_render_data = self._prev_move_data_rects

        # Render moves on the stack
        for data, rects in stack_render_data.items():
            for rect in rects:
                _render_move(data.move, data.time_left, rect, screen)

        # Render moves under characters
        for data in current_move_datas:
            if not data.under_char:
                continue
            rects = scene.layout.get_rects(data)
            assert len(rects) == 1
            _render_move(data.move, None, rects[0], screen,
                         small_text=True, CPU_not_time=True)


def _render_combat_options(scene: CombatScene, screen: Screen) -> None:
    x, font_size, spacing = rescale_horizontal(450, 35, 50)
    y, = rescale_vertical(700)

    text = ['{}: {} ({} rounds, {} CPU)'.format(
        i + 1, m.subroutine.description(), m.subroutine.time_to_resolve(),
        m.subroutine.cpu_slots())
        for i, m in enumerate(scene.available_moves())]

    screen.render_texts(text, font_size=font_size, x=x, y=y,
                        color=GREEN, spacing=spacing)


def _render_character(info: CharacterInfo, screen: Screen, rect: Rect) -> None:
    screen.render_image(info.image_path, rect.x, rect.y, rect.w, rect.h)

    font_size = rescale_vertical(30)[0]
    vert_spacing = font_size
    x = rect.x

    # health above image
    health_bar = 'HP: {} / {}'.format(info.health, info.max_health)

    y = rect.y - vert_spacing
    screen.render_text(health_bar, font_size, x, y, GREEN, w=rect.w)

    # Draw shields if they exist above health
    if info.shields > 0:
        y = rect.y - 2 * vert_spacing
        screen.render_text('Shield: {}'.format(info.shields), font_size, x, y,
                           LIGHT_BLUE, w=rect.w)

    # Status effects above health/shields
    y -= vert_spacing * (len(info.active_effects) + 1)
    for effect in info.active_effects:
        y += vert_spacing
        screen.render_text(effect.label, font_size, x, y, RED, w=rect.w)

    # Name below image
    y = rect.y + rect.h + 0.5 * vert_spacing
    screen.render_text(info.description, font_size, x, y, GREEN, w=rect.w)

    # CPU slots below name
    y += vert_spacing
    cpu_bar = 'CPU: {} / {}'.format(info.cpu, info.max_cpu)
    screen.render_text(cpu_bar, font_size, x, y, YELLOW, w=rect.w)

    # Selection box
    if info.is_selected:
        screen.render_rect(rect, RED, 2)

    # X out dead character
    if info.is_dead:
        start = rect.x, rect.y
        end = rect.x + rect.w, rect.y + rect.h
        screen.render_line(start, end, RED, 4)

        start, end = (start[0], end[1]), (end[0], start[1])
        screen.render_line(start, end, RED, 4)
