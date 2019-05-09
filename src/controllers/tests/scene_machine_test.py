from controllers.controller_factory import build_controller
from controllers.scene_machine import SceneMachine
from controllers.settings_controller import SettingsController
from events.events_base import BasicEvents, NewSceneEvent
from models.scenes.decision_scene import DecisionScene
from models.scenes.scene_examples import loading_scene


def test_toggle_settings():
    machine = SceneMachine()

    # This is the scene to return to after the temporary scene is toggled twice.
    initial_scene = DecisionScene('dummy scene', {}, inventory_available=True)
    initial_controller_type = type(build_controller(initial_scene))
    assert initial_controller_type is not SettingsController
    machine.notify(NewSceneEvent(initial_scene))

    assert isinstance(machine.controller, initial_controller_type)

    machine.notify(BasicEvents.SETTINGS)
    assert isinstance(machine.controller, SettingsController)

    machine.notify(BasicEvents.SETTINGS)
    assert isinstance(machine.controller, initial_controller_type)


def test_toggler_settings_then_inventory_stays_settings():
    machine = SceneMachine()

    # This is the scene to return to after the temporary scene is toggled twice.
    initial_scene = loading_scene()
    machine.notify(NewSceneEvent(initial_scene))

    assert not isinstance(machine.controller, SettingsController)
    machine.notify(BasicEvents.SETTINGS)
    assert isinstance(machine.controller, SettingsController)

    machine.notify(BasicEvents.INVENTORY)
    assert isinstance(machine.controller, SettingsController)
