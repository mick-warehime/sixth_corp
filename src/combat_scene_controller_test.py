from character_base import Character
from combat_scene import CombatScene
from combat_scene_controller import CombatSceneController
from events_utils import simulate_key_press
from unittest import mock
from unittest import TestCase
from world import World


def create_combat_controller(enemy):
    scene = CombatScene()
    scene.set_enemy(enemy)
    mock_screen = mock.Mock()
    world = World()
    return CombatSceneController(mock_screen, world, scene)


class CombatSceneControllerTest(TestCase):

    @mock.patch('pygame_view.pygame')
    def test_game_over(self, mock_pygame):
        ctl = create_combat_controller(enemy=Character(10))

        self.assertFalse(ctl.model.is_game_over())

    @mock.patch('pygame_view.pygame')
    def test_kill_enemy(self, mock_pygame):
        ctl = create_combat_controller(enemy=Character(5))
        self.assertFalse(ctl.model.scene.is_resolved())

        simulate_key_press('2')

        self.assertTrue(ctl.model.scene.is_resolved())
