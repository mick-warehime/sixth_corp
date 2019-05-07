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
            # Draw selection
            if info.is_selected:
                screen.render_rect(rect, RED, 2)


def _render_character(info: CharacterInfo, screen: Screen, rect: Rect) -> None:
    screen.render_image(info.image_path, rect.x, rect.y, rect.w, rect.h)

    font_size = rescale_vertical(30)[0]
    vert_spacing = font_size
    x = rect.x
    # Draw shields if they exist above image

    if info.shields > 0:
        y = rect.y - 2 * vert_spacing
        screen.render_text('Shield: {}'.format(info.shields), font_size, x, y,
                           LIGHT_BLUE, w=rect.w)

    # Draw health above image
    health_bar = 'HP: {} / {}'.format(info.health, info.max_health)

    y = rect.y - vert_spacing
    screen.render_text(health_bar, font_size, x, y, GREEN, w=rect.w)

    # Draw status effects
    y -= vert_spacing * (len(info.active_effects) + 1)
    for effect in info.active_effects:
        y += vert_spacing
        screen.render_text(effect.label, font_size, x, y, RED, w=rect.w)

    # Draw name below image
    y = rect.y + rect.h + 0.5 * vert_spacing
    screen.render_text(info.description, font_size, x, y, GREEN, w=rect.w)

    # Draw CPU slots below name
    y += vert_spacing
    cpu_bar = 'CPU: {} / {}'.format(info.cpu, info.max_cpu)
    screen.render_text(cpu_bar, font_size, x, y, YELLOW, w=rect.w)
