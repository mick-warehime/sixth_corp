from character_base import Character
from decision_scene import DecisionScene, DecisionOption
from typing import Dict


class CombatScene(DecisionScene):

    def __init__(self, enemy: Character,
                 choices: Dict[str, DecisionOption]) -> None:
        super().__init__('', choices)
        self.enemy = enemy
