from characters.character_base import Character
from characters.player import get_player
from characters.states import Attributes
from data.colors import GREEN, RED
from scenes.combat_scene import CombatScene
from views.artists.scene_artist_base import SceneArtist
from views.screen_base import Screen


class CharacterArtist(SceneArtist):
    """Draws Characters on the screen."""

    def render(self, screen: Screen, scene: CombatScene) -> None:
        player = get_player()
        enemy = scene.enemy()
        for char in [player, enemy]:
            self._render_character(char, screen)
            self._render_selected(char, screen, scene)

    def _render_character(self, character: Character, screen: Screen) -> None:
        self._render_image(character, screen)
        self._render_health(character, screen)
        self._render_name(character, screen)

    def _render_image(self, character: Character, screen: Screen) -> None:
        pos = character.rect
        screen.render_image(character.image_path, pos.x, pos.y, pos.w, pos.h)

    def _render_health(self, character: Character, screen: Screen) -> None:
        pos = character.rect
        health = character.status.get_attribute(Attributes.HEALTH)
        max_health = character.status.get_attribute(Attributes.MAX_HEALTH)
        health_bar = '{} / {}'.format(health, max_health)
        x = int(pos.x + pos.w / 4.0)
        y = pos.y - 40
        screen.render_text(health_bar, 30, x, y, GREEN)

    def _render_name(self, character: Character, screen: Screen) -> None:
        pos = character.rect
        x = int(pos.x + pos.w / 4.0)
        y = pos.y + 40 + pos.h
        screen.render_text(character.description(), 30, x, y, GREEN)

    def _render_selected(self, character: Character, screen: Screen,
                         scene: CombatScene) -> None:
        if character == scene.selected:
            pos = character.rect
            screen.render_rect(pos.x, pos.y, pos.w, pos.h, RED, 2)
