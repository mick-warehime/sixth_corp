import random

import pytest

from controllers.combat_scene_controller import CombatSceneController
from controllers.decision_scene_controller import DecisionSceneController
from controllers.game import Game, initialize_pygame
from events import event_utils
from events.events_base import EventManager
from scenes.combat_scene import CombatScene
from scenes.decision_scene import DecisionScene

# Needs to be called for game to run.
initialize_pygame(no_UI=True)
# To ensure determinism.
random.seed(11)

decision_scene = DecisionScene('dummy prompt', {})
combat_scene = CombatScene()


def setup_module():
    for e in EventManager.listeners.copy():
        EventManager.listeners.remove(e)


def test_initializing_game_adds_listeners():
    assert len(EventManager.listeners) == 0
    game = Game()  # noqa: F841
    assert len(EventManager.listeners) > 0


cases = [(combat_scene, CombatSceneController),
         (decision_scene, DecisionSceneController)]


@pytest.mark.parametrize("scene, expected_type", cases)
def test_changing_scenes_swaps_listener(scene, expected_type):
    game = Game()  # noqa: F841
    start_len = len(EventManager.listeners)

    event_utils.post_scene_change(scene)
    assert len(EventManager.listeners) <= start_len
    assert any(isinstance(l, expected_type) for l in EventManager.listeners)
