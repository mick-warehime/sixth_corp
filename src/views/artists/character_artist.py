from pygame.rect import Rect

from data.colors import GREEN, LIGHT_BLUE, RED, YELLOW
from models.characters.character_base import Character
from models.characters.states import Attributes
from models.scenes.combat_scene import CombatScene
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.pygame_screen import Screen


class CharacterArtist(SceneArtist):
    """Draws Characters on the screen."""

    def render(self, screen: Screen, scene: Scene) -> None:
        assert isinstance(scene, CombatScene)
        for char in scene.characters():
            rects = scene.layout.get_rects(char)
            assert len(rects) == 1

            rect = rects[0]
            _render_character(char, screen, rect)
            # Draw selection
            if char == scene.selected_char:
                screen.render_rect(rect, RED, 2)


def _render_character(character: Character, screen: Screen, rect: Rect) -> None:
    screen.render_image(character.image_path, rect.x, rect.y, rect.w, rect.h)

    font_size = rescale_vertical(30)[0]
    vert_spacing = font_size
    x = rect.x
    # Draw shields if they exist above image
    shields = character.status.get_attribute(Attributes.SHIELD)
    if shields > 0:
        y = rect.y - 3 * vert_spacing
        screen.render_text('Shield: {}'.format(shields), font_size, x, y,
                           LIGHT_BLUE, w=rect.w)

    # Draw health above image
    health = character.status.get_attribute(Attributes.HEALTH)
    max_health = character.status.get_attribute(Attributes.MAX_HEALTH)
    health_bar = 'HP: {} / {}'.format(health, max_health)

    y = rect.y - 2 * vert_spacing
    screen.render_text(health_bar, font_size, x, y, GREEN, w=rect.w)

    # Draw CPU slots above image
    cpu = character.status.get_attribute(Attributes.CPU_AVAILABLE)
    max_cpu = character.status.get_attribute(Attributes.MAX_CPU)
    y += vert_spacing
    cpu_bar = 'CPU: {} / {}'.format(cpu, max_cpu)
    screen.render_text(cpu_bar, font_size, x, y, YELLOW, w=rect.w)

    # Draw name below image
    y = rect.y + rect.h
    screen.render_text(character.description(), font_size, x, y, GREEN,
                       w=rect.w)
