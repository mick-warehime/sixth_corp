import random
from collections import Counter

import pytest

from models.scenes.skill_checks import Difficulty

# To ensure deterministic tests
random.seed(0)


@pytest.mark.parametrize("base,modifier,expected",
                         [(Difficulty.MODERATE, -2, Difficulty.VERY_HARD),
                          (Difficulty.IMPOSSIBLE, -1, Difficulty.IMPOSSIBLE),
                          (Difficulty.IMPOSSIBLE, 2, Difficulty.HARD),
                          (Difficulty.MODERATE, 100, Difficulty.TRIVIAL)])
def test_difficulty_adjustments(base, modifier, expected):
    assert base.adjust(modifier) == expected


@pytest.mark.parametrize('difficulty', [d for d in Difficulty])
def test_skill_check_statistics(difficulty):
    num_calls = 1000
    counts = Counter()

    for _ in range(num_calls):
        if difficulty.sample_success():
            counts['success'] += 1
        else:
            counts['failure'] += 1

    assert sum(counts.values()) == num_calls
    error = counts['success'] / num_calls - difficulty.success_prob
    assert abs(error) < 50 / num_calls
