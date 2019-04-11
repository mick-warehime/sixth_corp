from os.path import dirname, abspath
import os
from typing import List

from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.game import initialize_pygame, Game
from controllers.inputs.keybindings import Keybindings
from controllers.inputs.keyboard import Keyboard
from events import event_utils
from events.events_base import EventManager, EventTypes
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene, DecisionOption

# Ensure that working directory is sixth_corp
from views.view_manager import ViewManager

os.chdir(dirname(dirname(dirname(abspath(__file__)))))

initialize_pygame(no_UI=True)


def _get_active_controller():
    listeners = [l for l in EventManager.listeners if isinstance(l, Controller)]
    assert len(listeners) == 1
    return listeners[0]


def test_making_choices_removes_listener():
    game = Game()  # noqa: F841

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


def _keys_for_event(event: EventTypes, keyboard: Keyboard) -> List[str]:
    return [k for k, v in keyboard.bindings.bindings.items() if v == event]


def test_press_debug_in_decision_scene_has_no_effect():
    game = Game()
    view_manager = ViewManager()

    event_utils.post_scene_change(DecisionScene('dummy', {}))

    assert isinstance(game.scene_machine.controller, DecisionSceneController)
    assert view_manager.current_view is not None

    EventManager.post(EventTypes.DEBUG)
    EventManager.post(EventTypes.TICK)
