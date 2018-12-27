import pygame
from character_base import Character
from pygame_view import PygameView
from typing import List

from states import Attribute


class CombatSceneView(PygameView):

    def __init__(self, screen: pygame.Surface, player: Character,
                 enemy: Character) -> None:
        super(CombatSceneView, self).__init__(screen)
        self._text_fmt = 'Combat Scene\n\nPlayer Life: {}' \
                         ', Enemy Life: {}\n\n1: Do 1 damage\n2: Do 5 damage'
        self.texts: List[str] = None
        self.player = player
        self.enemy = enemy

    def render(self) -> None:
        self._update(self.player, self.enemy)
        self.render_text()

    def _update(self, player: Character, enemy: Character) -> None:
        player_health = player.get_attribute(Attribute.HEALTH)
        enemy_health = enemy.get_attribute(Attribute.HEALTH)
        self.texts = self._text_fmt.format(player_health, enemy_health).split(
            '\n')
