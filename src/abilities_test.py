import random

import pytest

from abilities import Difficulty, skill_check

# To ensure deterministic tests
random.seed(0)


@pytest.mark.parametrize("base,modifier,expected",
                         [(Difficulty.MODERATE, -2, Difficulty.VERY_HARD),
                          (Difficulty.IMPOSSIBLE, -1, Difficulty.IMPOSSIBLE),
                          (Difficulty.IMPOSSIBLE, 2, Difficulty.HARD),
                          (Difficulty.MODERATE, 100, Difficulty.TRIVIAL)])
def test_difficulty_adjustments(base, modifier, expected):
    assert base.adjust(modifier) == expected


@pytest.mark.parametrize('difficulty', Difficulty)
def test_skill_check_statistics(difficulty):
    num_calls = 1000
    call_counts = {'success': 0, 'failure': 0}

    def on_success(world):
        call_counts['success'] += 1
        return None

    def on_failure(world):
        call_counts['failure'] += 1
        return None

    scene_fun = skill_check(difficulty, on_success, on_failure)

    for _ in range(num_calls):
        scene_fun(None)

    assert sum(call_counts.values()) == num_calls
    error = call_counts['success'] / num_calls - difficulty.success_prob
    assert abs(error) < 50 / num_calls
