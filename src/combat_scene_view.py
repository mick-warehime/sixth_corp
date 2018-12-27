import pygame
from character_base import Character
from decision_scene_view import DecisionSceneView
from typing import Dict

from states import Attribute


class CombatSceneView(DecisionSceneView):
    def __init__(self, screen: pygame.Surface, player: Character,
                 enemy: Character, options: Dict[str, str]) -> None:
        self.player = player
        self.enemy = enemy
        super().__init__(screen, self._main_text, options)

    def _main_text(self) -> str:
        player_health = self.player.get_attribute(Attribute.HEALTH)
        enemy_health = self.enemy.get_attribute(Attribute.HEALTH)
        text_fmt = 'Combat Scene\n\nPlayer Life: {}, Enemy Life: {}'
        return text_fmt.format(player_health, enemy_health)
