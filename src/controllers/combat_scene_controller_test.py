from unittest import TestCase, mock

from characters.effects import IncrementAttribute
from characters.states import Attributes
from combat.combat_test_utils import create_enemy
from controllers.combat_scene_controller import CombatSceneController
from events.event_utils import simulate_key_press, simulate_mouse_click
from scenes.combat_scene import CombatScene


def create_combat_controller(enemy):
    scene = CombatScene()
    scene.set_enemy(enemy)
    return CombatSceneController(scene)


def select_enemy(enemy):
    cx, cy = enemy.rect.center
    simulate_mouse_click(cx, cy)


class CombatSceneControllerTest(TestCase):

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_game_over(self, mock_pygame, mock_loader):
        ctl = create_combat_controller(enemy=create_enemy(10))

        self.assertFalse(ctl.scene.is_game_over())

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_kill_enemy(self, mock_pygame, mock_loader):
        health = 2
        enemy = create_enemy(health)
        ctl = create_combat_controller(enemy)
        self.assertFalse(ctl.scene.is_resolved())

        IncrementAttribute(enemy, Attributes.HEALTH, -health).execute()

        self.assertTrue(ctl.scene.is_resolved())

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_selected_enemy(self, mock_pygame, mock_loader):
        enemy = create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        select_enemy(enemy)

        self.assertIsNotNone(ctl.scene.selected_char)
        self.assertEqual(ctl.scene.selected_char, enemy)

        simulate_mouse_click(-1000, -1000)
        self.assertIsNone(ctl.scene.selected_char)

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_enemy_unselected_after_move(self, mock_pygame, mock_loader):
        enemy = create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        select_enemy(enemy)

        self.assertIsNotNone(ctl.scene.selected_char)
        self.assertEqual(ctl.scene.selected_char, enemy)

        simulate_key_press('1')
        self.assertIsNone(ctl.scene.selected_char)

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_reclick_unselects(self, mock_pygame, mock_loader):
        enemy = create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        select_enemy(enemy)

        self.assertIsNotNone(ctl.scene.selected_char)
        self.assertEqual(ctl.scene.selected_char, enemy)

        select_enemy(enemy)
        self.assertIsNone(ctl.scene.selected_char)

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_click_nothing_selects_nothing(self, mock_pygame, mock_loader):
        enemy = create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        simulate_mouse_click(-100, -100)

        self.assertIsNone(ctl.scene.selected_char)
