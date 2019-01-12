from typing import List, Sequence

from characters.character_base import Character
from characters.states import Attribute
from combat.moves_base import Move
from views.pygame_view import PygameView
from world.world import get_location


class CombatSceneView(PygameView):

    def __init__(self) -> None:
        super(CombatSceneView, self).__init__(
            get_location().background_image_path)
        self.texts: List[str] = None
        self._targetting_enabled = False
        self._target_descriptions: List[str] = []

    def render_view(self, player: Character, enemy: Character,
                    selected: Character) -> None:
        super().render()
        self.render_text(self.texts)
        self.render_character(player)
        self.render_character(enemy)
        if selected is not None:
            pos = selected.position
            self.draw_rect(pos.x, pos.y, pos.w, pos.h)
        self.render_health(player)
        self.render_health(enemy)

    def render_character(self, character: Character) -> None:
        pos = character.position
        self.render_image(character.image_path, pos.x, pos.y, pos.w, pos.h)

    def _combat_options(self, moves: Sequence[Move]) -> List[str]:
        return ['{} - {}'.format(i + 1, m.ability.description())
                for i, m in enumerate(moves)]

    def update(self, player: Character, enemy: Character,
               moves: Sequence[Move], selected: Character) -> None:
        options = self._combat_options(moves)
        self.texts = options
        self.render_view(player, enemy, selected)

    def render_health(self, char: Character) -> None:
        pos = char.position
        health = char.get_attribute(Attribute.HEALTH)
        max_health = char.get_attribute(Attribute.MAX_HEALTH)
        health_bar = '{} / {}'.format(health, max_health)
        rasterized = self._smallfont.render(health_bar, True, (0, 255, 0))
        x = int(pos.x + pos.w / 4.0)
        y = pos.y - 40
        self.screen.blit(rasterized, (x, y))
        self.update_display()
