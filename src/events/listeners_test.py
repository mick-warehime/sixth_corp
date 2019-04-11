from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.controller_factory import build_controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.game import Game
from controllers.scene_machine import SceneMachine
from events import event_utils
from events.events_base import EventManager, DecisionEvent
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene, DecisionOption
from models.scenes.scene_examples import loading_scene


def test_initializing_game_adds_listeners():
    assert len(EventManager.listeners) == 0
    game = Game()  # noqa: F841
    assert len(EventManager.listeners) > 0


def test_changing_scenes_removes_previous_listener():
    assert len(EventManager.listeners) == 0
    machine = SceneMachine()  # noqa: F841
    assert len(EventManager.listeners) == 1

    initial_scene = loading_scene()
    initial_controller_type = type(build_controller(initial_scene))

    final_scene = CombatScene()
    final_controller_type = type(build_controller(final_scene))

    event_utils.post_scene_change(initial_scene)

    assert any(isinstance(l, initial_controller_type)
               for l in EventManager.listeners)
    assert not any(isinstance(ctl, final_controller_type)
                   for ctl in EventManager.listeners)

    event_utils.post_scene_change(final_scene)

    assert any(isinstance(l, final_controller_type)
               for l in EventManager.listeners)
    assert not any(isinstance(ctl, initial_controller_type)
                   for ctl in EventManager.listeners)


def _get_active_controller():
    listeners = [l for l in EventManager.listeners if isinstance(l, Controller)]
    assert len(listeners) == 1
    return listeners[0]


def test_making_choices_removes_listener():
    machine = SceneMachine()  # noqa: F841

    def second_scene() -> DecisionScene:
        options = {'1': DecisionOption('third scene', CombatScene)}
        return DecisionScene('second scene', options)

    options_0 = {'s': DecisionOption('load next scene', second_scene)}
    scene_0 = DecisionScene('first scene', options_0)

    event_utils.post_scene_change(scene_0)
    num_listeners = len(EventManager.listeners)
    ctl = _get_active_controller()
    assert isinstance(ctl, DecisionSceneController)
    # we must remove references otherwise EventManager will keep this listener
    del ctl

    event_utils.simulate_key_press('s')
    del scene_0

    assert len(EventManager.listeners) == num_listeners

    ctl = _get_active_controller()
    assert isinstance(ctl, DecisionSceneController)
    del ctl

    event_utils.simulate_key_press('1')

    assert len(EventManager.listeners) == num_listeners
    ctl = _get_active_controller()
    assert isinstance(ctl, CombatSceneController)
    del ctl
