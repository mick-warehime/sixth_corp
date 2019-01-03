from typing import List
from models.character_base import Character
from world.world import get_location
from views.pygame_view import PygameView
from models.states import Attribute

_COMBAT_BACKGROUND = 'src/images/background_combat.png'


class CombatSceneView(PygameView):

    def __init__(self) -> None:
        super(CombatSceneView, self).__init__(get_location().background_image_path)
        self._header_fmt = 'Combat Scene\n\nPlayer Life: {}, Enemy Life: {}'
        self.texts: List[str] = None

    def render(self) -> None:
        super().render()
        self.render_text(self.texts)

    def update(self, player: Character, enemy: Character) -> None:
        player_health = player.get_attribute(Attribute.HEALTH)
        enemy_health = enemy.get_attribute(Attribute.HEALTH)
        header = self._header_fmt.format(player_health, enemy_health).split(
            '\n')
        moves = player.get_moves(enemy)
        options = []
        for i in range(len(moves)):
            options.append('{}: {}'.format(i, moves[i].describe()))
        self.texts = header + options
        self.render()
