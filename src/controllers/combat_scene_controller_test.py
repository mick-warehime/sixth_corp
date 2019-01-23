from unittest import TestCase, mock

from characters.effects import IncrementAttribute
from characters.states import Attributes
from combat.combat_test_utils import create_enemy
from controllers.combat_scene_controller import CombatSceneController
from events.event_utils import simulate_mouse_click
from scenes.combat_scene import CombatScene


def create_combat_controller(enemy):
    scene = CombatScene()
    scene.set_enemy(enemy)
    return CombatSceneController(scene)


def select_enemy(enemy):
    cx, cy = enemy.position.center()
    simulate_mouse_click(cx, cy)


class CombatSceneControllerTest(TestCase):

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_game_over(self, mock_update, mock_loader, mock_pygame):
        ctl = create_combat_controller(enemy=create_enemy(10))

        self.assertFalse(ctl.scene.is_game_over())

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_kill_enemy(self, mock_update, mock_loader, mock_pygame):
        health = 2
        enemy = create_enemy(health)
        ctl = create_combat_controller(enemy)
        self.assertFalse(ctl.scene.is_resolved())

        IncrementAttribute(enemy, Attributes.HEALTH, -health).execute()

        self.assertTrue(ctl.scene.is_resolved())
