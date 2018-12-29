from typing import List
from models.character_base import Character
from views.pygame_view import PygameView
from models.states import Attribute


class CombatSceneView(PygameView):

    def __init__(self) -> None:
        super(CombatSceneView, self).__init__()
        self._text_fmt = 'Combat Scene\n\nPlayer Life: {}' \
                         ', Enemy Life: {}\n\n1: Do 1 damage\n2: Do 5 damage'
        self.texts: List[str] = None

    def render(self) -> None:
        self.render_text()

    def update(self, player: Character, enemy: Character) -> None:
        player_health = player.get_attribute(Attribute.HEALTH)
        enemy_health = enemy.get_attribute(Attribute.HEALTH)
        self.texts = self._text_fmt.format(player_health, enemy_health).split(
            '\n')
        self.render()
