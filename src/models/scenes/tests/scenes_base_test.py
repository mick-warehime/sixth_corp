"""Tests for scenes_base.py"""
import random
from collections import Counter
from unittest.mock import Mock

import pytest

from models.scenes.scenes_base import (ProbabilisticResolution, Resolution,
                                       Scene)


def _mock_resolution(label) -> Mock:
    scene = Mock(Scene, label=label)
    return Mock(Resolution, label=label, next_scene=lambda: scene)


def test_probabilistic_resolution_correct_probabilities():
    random.seed(11)  # to ensure determinism
    weights = 0, 2, 1, 5
    res_weights = [(_mock_resolution(label=k), w)
                   for k, w in enumerate(weights)]

    counter = Counter()
    num_samples = 1000
    for _ in range(num_samples):
        resolution = ProbabilisticResolution(res_weights)
        counter[resolution.next_scene().label] += 1

    actual = [counter[k] / num_samples for k in range(len(weights))]
    total = sum(weights)
    expected = [w / total for w in weights]

    assert pytest.approx(expected, abs=0.1) == actual
