from typing import List
from models.character_base import Character
from world.world import get_location
from views.pygame_view import PygameView
from models.states import Attribute

_COMBAT_BACKGROUND = 'src/images/background_combat.png'


class CombatSceneView(PygameView):

    def __init__(self) -> None:
        super(CombatSceneView, self).__init__(
            get_location().background_image_path)
        self.texts: List[str] = None

    def render(self) -> None:
        super().render()
        self.render_text(self.texts)

    def _scene_description(self, player: Character, enemy: Character):
        texts = [
            'You are fighting a dreaded {}.'.format(enemy.__class__.__name__),
            'Your health: {}'.format(player.get_attribute(Attribute.HEALTH)),
            'Enemy health: {}'.format(enemy.get_attribute(Attribute.HEALTH)),
            ''
        ]
        return texts

    def update(self, player: Character, enemy: Character) -> None:
        header = self._scene_description(player, enemy)
        moves = player.get_moves(enemy)
        options = []
        for i in range(len(moves)):
            options.append('{}: {}'.format(i, moves[i].describe()))
        self.texts = header + options
        self.render()
