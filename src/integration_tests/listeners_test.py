import random
from unittest import TestCase, mock

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


class IntegrationTest(TestCase):

    def setUp(self):
        for e in EventManager.listeners.copy():
            EventManager.listeners.remove(e)

    @mock.patch('views.pygame_screen.pygame')
    def test_initializing_game_adds_listeners(self, mock_pygame):
        assert len(EventManager.listeners) == 0
        game = Game()  # noqa: F841
        assert len(EventManager.listeners) > 0

    @mock.patch('views.pygame_screen.pygame')
    def test_changing_combat_scenes_swaps_listener(self, mock_pygame):
        game = Game()  # noqa: F841
        start_len = len(EventManager.listeners)

        event_utils.post_scene_change(combat_scene)
        assert len(EventManager.listeners) <= start_len
        assert any(isinstance(l, CombatSceneController) for l in EventManager.listeners)

    @mock.patch('views.pygame_screen.pygame')
    def test_changing_decision_scenes_swaps_listener(self, mock_pygame):
        game = Game()  # noqa: F841
        start_len = len(EventManager.listeners)

        event_utils.post_scene_change(decision_scene)
        assert len(EventManager.listeners) <= start_len
        assert any(isinstance(l, DecisionSceneController) for l in EventManager.listeners)
