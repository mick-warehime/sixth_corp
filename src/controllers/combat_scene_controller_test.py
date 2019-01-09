from unittest import TestCase, mock

from characters.character_base import Character
from characters.enemy_base import Enemy
from controllers.combat_scene_controller import CombatSceneController
from events.event_utils import simulate_key_press, simulate_mouse_click
from scenes.combat_scene import CombatScene


def create_combat_controller(enemy):
    scene = CombatScene()
    scene.set_enemy(enemy)
    return CombatSceneController(scene)


class CombatSceneControllerTest(TestCase):

    @mock.patch('views.pygame_view.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_game_over(self, mock_update, mock_loader, mock_pygame):
        ctl = create_combat_controller(enemy=Character(10))

        self.assertFalse(ctl.model.is_game_over())

    @mock.patch('views.pygame_view.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_kill_enemy(self, mock_update, mock_loader, mock_pygame):
        ctl = create_combat_controller(enemy=Character(2))
        self.assertFalse(ctl.model.scene.is_resolved())

        simulate_key_press('1')
        simulate_key_press('1')

        self.assertTrue(ctl.model.scene.is_resolved())

    @mock.patch('views.pygame_view.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_selected_enemy(self, mock_update, mock_loader, mock_pygame):
        enemy = Enemy(2, name='test dummy')
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.selected_character)

        cx, cy = enemy.position.center()
        simulate_mouse_click(cx, cy)

        self.assertIsNotNone(ctl.selected_character)
        self.assertEqual(ctl.selected_character, enemy)

        simulate_mouse_click(-1000, -1000)
        self.assertIsNone(ctl.selected_character)

    @mock.patch('views.pygame_view.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_reclick_unselects(self, mock_update, mock_loader, mock_pygame):
        enemy = Enemy(2, name='test dummy')
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.selected_character)

        cx, cy = enemy.position.center()
        simulate_mouse_click(cx, cy)

        self.assertIsNotNone(ctl.selected_character)
        self.assertEqual(ctl.selected_character, enemy)

        simulate_mouse_click(cx, cy)
        self.assertIsNone(ctl.selected_character)

    @mock.patch('views.pygame_view.pygame')
    @mock.patch('views.pygame_images.load_image')
    @mock.patch('controllers.combat_scene_controller.CombatSceneController.update')
    def test_click_nothing_selects_nothing(self, mock_update, mock_loader, mock_pygame):
        enemy = Enemy(2, name='test dummy')
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.selected_character)

        simulate_mouse_click(-100, -100)

        self.assertIsNone(ctl.selected_character)
