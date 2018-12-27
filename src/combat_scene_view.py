import pygame
from character_base import Character
from character_state import State
from pygame_view import PygameView
from typing import List


class CombatSceneView(PygameView):

    def __init__(self, screen: pygame.Surface) -> None:
        super(CombatSceneView, self).__init__(screen)
        self._text_fmt = 'Combat Scene\n\nPlayer Life: {}' \
                         ', Enemy Life: {}\n\n1: Do 1 damage\n2: Do 5 damage'
        self.texts: List[str] = None

    def render(self) -> None:
        self.render_text()

    def update(self, player: Character, enemy: Character) -> None:
        player_health = player.get_state(State.HEALTH)
        enemy_health = enemy.get_state(State.HEALTH)
        self.texts = self._text_fmt.format(player_health, enemy_health).split('\n')
        self.render()
