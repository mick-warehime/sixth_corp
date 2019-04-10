import pytest

from controllers.controller_factory import build_controller
from controllers.inventory_controller import InventoryController
from controllers.scene_machine import SceneMachine
from controllers.settings_controller import SettingsController
from events.events_base import EventTypes, NewSceneEvent
from models.scenes.scene_examples import loading_scene

cases = [(EventTypes.SETTINGS, SettingsController),
         (EventTypes.INVENTORY, InventoryController)]


@pytest.mark.parametrize('event_type,controller_type', cases)
def test_toggle_temporary_scene(event_type, controller_type):
    machine = SceneMachine()

    # This is the scene to return to after the temporary scene is toggled twice.
    initial_scene = loading_scene()
    initial_controller_type = type(build_controller(initial_scene))
    assert initial_controller_type is not controller_type
    machine.notify(NewSceneEvent(initial_scene))

    assert isinstance(machine.controller, initial_controller_type)

    machine.notify(event_type)
    assert isinstance(machine.controller, controller_type)

    machine.notify(event_type)
    assert isinstance(machine.controller, initial_controller_type)


def test_toggler_settings_then_inventory_stays_settings():
    machine = SceneMachine()

    # This is the scene to return to after the temporary scene is toggled twice.
    initial_scene = loading_scene()
    machine.notify(NewSceneEvent(initial_scene))

    assert not isinstance(machine.controller, SettingsController)
    machine.notify(EventTypes.SETTINGS)
    assert isinstance(machine.controller, SettingsController)

    machine.notify(EventTypes.INVENTORY)
    assert isinstance(machine.controller, SettingsController)
