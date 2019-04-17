from pygame.rect import Rect

from data.colors import GREEN, RED, YELLOW
from models.characters.character_base import Character
from models.characters.states import Attributes
from models.scenes.combat_scene import CombatScene
from models.scenes.scenes_base import Scene
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

    # Draw health
    health = character.status.get_attribute(Attributes.HEALTH)
    max_health = character.status.get_attribute(Attributes.MAX_HEALTH)
    health_bar = 'HP: {} / {}'.format(health, max_health)
    x = rect.centerx-rect.w/8
    y = rect.y - 60
    screen.render_text(health_bar, 30, x, y, GREEN)

    # Draw CPU slots
    cpu = character.status.get_attribute(Attributes.CPU_AVAILABLE)
    max_cpu = character.status.get_attribute(Attributes.MAX_CPU)
    y += 30
    cpu_bar = 'CPU: {} / {}'.format(cpu, max_cpu)
    screen.render_text(cpu_bar, 30, x, y, YELLOW)

    # Draw name
    y += 30 + rect.h
    screen.render_text(character.description(), 30, x, y, GREEN)
