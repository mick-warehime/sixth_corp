"""Implementation of skill checks."""
import random
from enum import Enum
from typing import Sequence, Union

from scenes_base import SceneConstructor, Scene
from states import Ability
from world import World


class Difficulty(Enum):
    TRIVIAL = -3
    VERY_EASY = -2
    EASY = -1
    MODERATE = 0
    HARD = 1
    VERY_HARD = 2
    IMPOSSIBLE = 3

    @property
    def success_prob(self) -> float:
        return _difficulty_probs[self]

    def adjust(self, modifier: int) -> 'Difficulty':
        new_value = self.value + modifier
        new_value = min(new_value, 3)
        new_value = max(new_value, -3)
        return Difficulty(new_value)


_difficulty_probs = {k: v for k, v in
                     zip(Difficulty, [1, 7 / 8, 3 / 4, 1 / 2, 1 / 4, 1 / 8, 0])}


def skill_check(difficulty: Difficulty, success: SceneConstructor,
                failure: SceneConstructor,
                modifiers: Union[Ability, Sequence[Ability]] = ()):
    """Returns a scene constructing function that implements a skill check.

    Args:
        difficulty: The base skill check difficulty.
        success: Constructor to call if skill check passes.
        failure: Constructor to call if skill check fails.
        modifiers: Ability(ies) that modify the skill check.
    """
    if isinstance(modifiers, Ability):
        modifiers = [modifiers]

    def scene_builder(world: World) -> Scene:
        modifier = 0
        for ability in modifiers:
            modifier += world.player.get_attribute(ability)
        effective_difficulty = difficulty.adjust(modifier)

        if random.random() < effective_difficulty.success_prob:
            return success(world)
        return failure(world)

    return scene_builder