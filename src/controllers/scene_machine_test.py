from unittest import TestCase, mock

from controllers.inventory_controller import InventoryController
from controllers.scene_machine import SceneMachine
from controllers.settings_controller import SettingsController
from events.events_base import EventTypes


class SceneMachineTest(TestCase):

    @mock.patch('views.pygame_screen.pygame')
    def test_toggle_settings(self, mock_pygame):
        machine = SceneMachine()

        self.assertNotIsInstance(machine.controller, SettingsController)
        machine.notify(EventTypes.SETTINGS)
        self.assertIsInstance(machine.controller, SettingsController)

    @mock.patch('views.pygame_screen.pygame')
    def test_toggle_inventory(self, mock_pygame):
        machine = SceneMachine()

        self.assertNotIsInstance(machine.controller, InventoryController)
        machine.notify(EventTypes.INVENTORY)
        self.assertIsInstance(machine.controller, InventoryController)

    @mock.patch('views.pygame_screen.pygame')
    def test_toggle_inventory_then_settings(self, mock_pygame):
        machine = SceneMachine()

        self.assertNotIsInstance(machine.controller, InventoryController)
        machine.notify(EventTypes.INVENTORY)
        self.assertIsInstance(machine.controller, InventoryController)
        machine.notify(EventTypes.SETTINGS)
        self.assertIsInstance(machine.controller, SettingsController)
        machine.notify(EventTypes.SETTINGS)
        self.assertNotIsInstance(machine.controller, SettingsController)
