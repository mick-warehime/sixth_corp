import os
from os.path import dirname

from controllers.controller_factory import build_controller
from controllers.game import Game
from controllers.scene_machine import SceneMachine
from events import event_utils
from events.events_base import EventManager
from models.scenes.combat_scene import CombatScene
from models.scenes.scene_examples import loading_scene

# Ensure that working directory is sixth_corp
os.chdir(dirname(dirname(dirname(dirname(os.path.abspath(__file__))))))


def test_initializing_game_adds_listeners():
    EventManager.listeners.clear()  # Other test modules may populate
    assert len(EventManager.listeners) == 0
    game = Game()  # noqa: F841
    assert len(EventManager.listeners) > 0


def test_changing_scenes_removes_previous_listener():
    EventManager.listeners.clear()  # Other tests/ modules may populate
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
