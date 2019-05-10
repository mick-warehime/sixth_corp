"""Implementation of skill checks."""
import random
from enum import Enum
from typing import Sequence, Union

from models.characters.player import get_player
from models.characters.states import Skills, AttributeType
from models.scenes.scenes_base import Scene, SceneConstructor


class Difficulty(Enum):
    IMPOSSIBLE = -3
    VERY_HARD = -2
    HARD = -1
    MODERATE = 0
    EASY = 1
    VERY_EASY = 2
    TRIVIAL = 3

    @property
    def success_prob(self) -> float:
        return _difficulty_probs[self]

    def adjust(self, modifier: int) -> 'Difficulty':
        new_value = self.value + modifier
        new_value = min(new_value, 3)
        new_value = max(new_value, -3)
        return Difficulty(new_value)

    def sample_success(self, *attrs: AttributeType) -> bool:
        """Sample success probability accounting for player skill modifiers."""
        player = get_player()
        modifier = sum(player.status.get_attribute(a)
                       for a in attrs)  # type: ignore
        effective_difficulty = self.adjust(modifier)

        return random.random() < effective_difficulty.success_prob


_difficulty_probs = {k: v for k, v in
                     zip(Difficulty, [0, 1 / 8, 1 / 4, 1 / 2, 3 / 4, 7 / 8, 1])}
