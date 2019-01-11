from typing import List, Sequence

from characters.character_base import Character
from characters.states import Attribute
from combat.combat_AI import Move
from views.pygame_view import PygameView
from world.world import get_location

_COMBAT_BACKGROUND = 'src/images/background_combat.png'


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

    def render_character(self, character: Character) -> None:
        pos = character.position
        self.render_image(character.image_path, pos.x, pos.y, pos.w, pos.h)

    def _scene_description(self, player: Character,
                           enemy: Character) -> List[str]:
        texts = [
            'You are fighting a dreaded {}.'.format(enemy.__class__.__name__),
            'Your health: {}'.format(player.get_attribute(Attribute.HEALTH)),
            'Enemy health: {}'.format(enemy.get_attribute(Attribute.HEALTH)),
            ''
        ]
        return texts

    def _combat_options(self, moves: Sequence[Move]) -> List[str]:
        return ['{} - {}'.format(i + 1, m.ability.description())
                for i, m in enumerate(moves)]

    def update(self, player: Character, enemy: Character,
               moves: Sequence[Move], selected: Character) -> None:
        header = self._scene_description(player, enemy)
        options = self._combat_options(moves)
        self.texts = header + options
        self.render_view(player, enemy, selected)
