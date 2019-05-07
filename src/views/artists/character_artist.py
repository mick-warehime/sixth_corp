from pygame.rect import Rect

from data.colors import GREEN, LIGHT_BLUE, RED, YELLOW
from models.scenes.combat_scene import CombatScene, CharacterInfo
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class CharacterArtist(SceneArtist):
    """Draws Characters on the screen."""

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)

        char_infos = [data for data in scene.layout.all_objects()
                      if isinstance(data, CharacterInfo)]

        for info in char_infos:
            rects = scene.layout.get_rects(info)
            assert len(rects) == 1

            rect = rects[0]
            _render_character(info, screen, rect)


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
