from models.character_base import Character
from scenes.combat_scene import CombatScene
from controllers.combat_scene_controller import CombatSceneController
from unittest import mock
from unittest import TestCase
from events.event_utils import simulate_key_press


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
        ctl = create_combat_controller(enemy=Character(5))
        self.assertFalse(ctl.model.scene.is_resolved())

        simulate_key_press('0')
        simulate_key_press('0')

        self.assertTrue(ctl.model.scene.is_resolved())
