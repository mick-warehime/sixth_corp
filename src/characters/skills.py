"""Implementation of skill checks."""
import random
from enum import Enum
from typing import Sequence, Union

from characters.player import get_player
from characters.states import Skill
from scenes.scenes_base import Scene, SceneConstructor


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


_difficulty_probs = {k: v for k, v in
                     zip(Difficulty, [0, 1 / 8, 1 / 4, 1 / 2, 3 / 4, 7 / 8, 1])}


def skill_check(
        difficulty: Difficulty, success: SceneConstructor,
        failure: SceneConstructor,
        modifiers: Union[Skill, Sequence[Skill]] = ()) -> SceneConstructor:
    """Returns a scene constructing function that implements a skill check.

    Args:
        difficulty: The base skill check difficulty.
        success: Constructor to call if skill check passes.
        failure: Constructor to call if skill check fails.
        modifiers: Ability(ies) that modify the skill check.
    """
    if isinstance(modifiers, Skill):
        modifiers = [modifiers]

    def scene_builder() -> Scene:
        modifier = sum(
            get_player().status.get_attribute(a) for a in modifiers)  # type: ignore
        effective_difficulty = difficulty.adjust(modifier)

        if random.random() < effective_difficulty.success_prob:
            return success()
        return failure()

    return scene_builder
