"""Implementation of skill checks."""
import random
from bisect import bisect_left
from enum import Enum
from itertools import accumulate
from typing import Any, Sequence, Tuple

from models.characters.player import get_player
from models.characters.states import AttributeType


class Difficulty(Enum):
    IMPOSSIBLE = 3
    VERY_HARD = 2
    HARD = 1
    MODERATE = 0
    EASY = -1
    VERY_EASY = -2
    TRIVIAL = -3

    @property
    def success_prob(self) -> float:
        return _difficulty_probs[self]

    def __add__(self, other: Any) -> 'Difficulty':
        if not isinstance(other, int):
            return NotImplemented
        return self._adjust(other)

    def __sub__(self, other: Any) -> 'Difficulty':
        if not isinstance(other, int):
            return NotImplemented
        return self._adjust(-other)

    def _adjust(self, modifier: int) -> 'Difficulty':
        """Adjust difficulty of check.

        Args:
            modifier: Integer modifier. Positive corresponds to more difficult.

        Returns:
            A new difficulty rating.

        """
        new_value = self.value + modifier
        new_value = min(new_value, 3)
        new_value = max(new_value, -3)
        return Difficulty(new_value)

    def sample_success(self, *attrs: AttributeType) -> bool:
        """Sample success probability accounting for player skill modifiers."""
        player = get_player()
        modifier = sum(player.status.get_attribute(a)
                       for a in attrs)  # type: ignore

        return random.random() < (self - modifier).success_prob


_difficulty_probs = {k: v for k, v in
                     zip(Difficulty, [0, 1 / 8, 1 / 4, 1 / 2, 3 / 4, 7 / 8, 1])}


def sample_weights(weighted_objects: Sequence[Tuple[Any, int]]) -> Any:
    """Return a probabilistic sample based on weights.

    Each possible outcome is given a positive weight. Its relative
    probability is its weight divided by the sum of all weights.

    Args:
        weighted_objects: A sequence of outcome,weight pairs.
    Returns:
        One of the outcomes in weighted_objects, with probability matching its
        relative weight.
    """

    assert weighted_objects, 'At least one resolution must be specified.'
    assert all(rw[1] >= 0 for rw in weighted_objects), (
        'weights must be positive, got {}'.format(weighted_objects))

    # Sample outcomes according to weight.
    cum_weights = list(accumulate((rw[1] for rw in weighted_objects),
                                  lambda a, b: a + b))
    num = random.randint(0, cum_weights[-1] - 1) + 1
    index = bisect_left(cum_weights, num)

    assert index < len(weighted_objects), (num, index)
    return weighted_objects[index][0]
