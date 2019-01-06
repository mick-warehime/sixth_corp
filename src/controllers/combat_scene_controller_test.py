from unittest import TestCase, mock

from characters.character_base import Character
from controllers.combat_scene_controller import CombatSceneController
from events.event_utils import simulate_key_press
from scenes.combat_scene import CombatScene


def create_combat_controller(enemy):
    scene = CombatScene()
    scene.set_enemy(enemy)
    return CombatSceneController(scene)


class CombatSceneControllerTest(TestCase):

    @mock.patch('views.pygame_view.pygame')
    def test_game_over(self, mock_pygame):
        ctl = create_combat_controller(enemy=Character(10))

        self.assertFalse(ctl.model.is_game_over())

    @mock.patch('views.pygame_view.pygame')
    def test_kill_enemy(self, mock_pygame):
        ctl = create_combat_controller(enemy=Character(2))
        self.assertFalse(ctl.model.scene.is_resolved())

        simulate_key_press('1')
        simulate_key_press('1')

        self.assertTrue(ctl.model.scene.is_resolved())
