from pygame.rect import Rect

from characters.character_base import Character
from characters.states import Attributes
from data.colors import GREEN, RED
from scenes.combat_scene import CombatScene
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen


class CharacterArtist(SceneArtist):
    """Draws Characters on the screen."""

    def render(self, screen: Screen, scene: CombatScene,
               layout: Layout) -> None:
        for char in scene.characters():
            rects = layout.get_rects(char)
            assert len(rects) == 1

            rect = rects[0]
            _render_character(char, screen, rect)
            # Draw selection
            if char == scene.selected_char:
                screen.render_rect(rect.x, rect.y, rect.w, rect.h, RED, 2)


def _render_character(character: Character, screen: Screen, rect: Rect) -> None:
    screen.render_image(character.image_path, rect.x, rect.y, rect.w, rect.h)

    # Draw health
    health = character.status.get_attribute(Attributes.HEALTH)
    max_health = character.status.get_attribute(Attributes.MAX_HEALTH)
    health_bar = '{} / {}'.format(health, max_health)
    x = int(rect.x + rect.w / 4.0)
    y = rect.y - 40
    screen.render_text(health_bar, 30, x, y, GREEN)

    # Draw name
    y += 40 + rect.h
    screen.render_text(character.description(), 30, x, y, GREEN)
