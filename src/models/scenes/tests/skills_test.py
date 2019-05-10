import random
from collections import Counter

import pytest

from models.scenes.skill_checks import Difficulty, sample_weights

# To ensure deterministic tests
random.seed(0)


@pytest.mark.parametrize("base,modifier,expected",
                         [(Difficulty.MODERATE, 2, Difficulty.VERY_HARD),
                          (Difficulty.IMPOSSIBLE, 1, Difficulty.IMPOSSIBLE),
                          (Difficulty.IMPOSSIBLE, -2, Difficulty.HARD),
                          (Difficulty.MODERATE, -100, Difficulty.TRIVIAL)])
def test_difficulty_adjustments(base, modifier, expected):
    assert base + modifier == expected


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


def test_sample_weights_correct_probability():
    random.seed(11)  # to ensure determinism
    weights = 0, 2, 1, 5
    keys_weights = list(enumerate(weights))

    counter = Counter()
    num_samples = 1000
    for _ in range(num_samples):
        counter[sample_weights(keys_weights)] += 1

    actual = [counter[k] / num_samples for k in range(len(weights))]
    total = sum(weights)
    expected = [w / total for w in weights]

    assert pytest.approx(expected, abs=0.1) == actual
