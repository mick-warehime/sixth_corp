from unittest import TestCase, mock

from characters.character_base import Character
from characters.character_examples import CharacterTypes
from characters.character_factory import build_character

from characters.effects import IncrementAttribute
from characters.states import Attributes
from controllers.combat_scene_controller import CombatSceneController
from events.event_utils import simulate_key_press, simulate_mouse_click
from scenes.combat_scene import CombatScene


def create_combat_controller(enemy):
    scene = CombatScene()
    scene.set_enemy(enemy)
    return CombatSceneController(scene)


def select_enemy(enemy, controller: CombatSceneController):
    rects = controller._view.layout.get_rects(enemy)
    assert len(rects) == 1

    simulate_mouse_click(*rects[0].center)


class CombatSceneControllerTest(TestCase):

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_game_over(self, mock_pygame, mock_loader):
        ctl = create_combat_controller(enemy=_create_enemy(10))

        self.assertFalse(ctl.scene.is_resolved())

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_kill_enemy(self, mock_pygame, mock_loader):
        health = 2
        enemy = _create_enemy(health)
        ctl = create_combat_controller(enemy)
        self.assertFalse(ctl.scene.is_resolved())

        IncrementAttribute(enemy, Attributes.HEALTH, -health).execute()

        self.assertTrue(ctl.scene.is_resolved())

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_selected_enemy(self, mock_pygame, mock_loader):
        enemy = _create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        select_enemy(enemy, ctl)

        self.assertIsNotNone(ctl.scene.selected_char)
        self.assertEqual(ctl.scene.selected_char, enemy)

        simulate_mouse_click(-1000, -1000)
        self.assertIsNone(ctl.scene.selected_char)

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_enemy_unselected_after_move(self, mock_pygame, mock_loader):
        enemy = _create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        select_enemy(enemy, ctl)

        self.assertIsNotNone(ctl.scene.selected_char)
        self.assertEqual(ctl.scene.selected_char, enemy)

        simulate_key_press('1')
        self.assertIsNone(ctl.scene.selected_char)

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_reclick_unselects(self, mock_pygame, mock_loader):
        enemy = _create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        select_enemy(enemy, ctl)

        self.assertIsNotNone(ctl.scene.selected_char)
        self.assertEqual(ctl.scene.selected_char, enemy)

        select_enemy(enemy, ctl)
        self.assertIsNone(ctl.scene.selected_char)

    @mock.patch('views.pygame_screen.pygame')
    @mock.patch('views.pygame_images.load_image')
    def test_click_nothing_selects_nothing(self, mock_pygame, mock_loader):
        enemy = _create_enemy(2)
        ctl = create_combat_controller(enemy)
        self.assertIsNone(ctl.scene.selected_char)

        simulate_mouse_click(-100, -100)

        self.assertIsNone(ctl.scene.selected_char)


def _create_enemy(health: int = 10) -> Character:
    enemy = build_character(CharacterTypes.DRONE.data)
    cur_val = enemy.status.get_attribute(Attributes.HEALTH)
    enemy.status.increment_attribute(Attributes.HEALTH, -cur_val)
    enemy.status.increment_attribute(Attributes.HEALTH, health)
    return enemy