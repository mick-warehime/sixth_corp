from controllers.combat_scene_controller import CombatSceneController
from controllers.game import Game
from controllers.scene_machine import SceneMachine
from events import event_utils
from events.events_base import EventManager
from models.scenes.combat_scene import CombatScene

from models.scenes.scene_examples import loading_scene


def test_initializing_game_adds_listeners():
    assert len(EventManager.listeners) == 0
    game = Game()  # noqa: F841
    assert len(EventManager.listeners) > 0


def test_changing_combat_scenes_removes_previous_listener():
    assert len(EventManager.listeners) == 0
    machine = SceneMachine()  # noqa: F841
    assert len(EventManager.listeners) == 1

    event_utils.post_scene_change(loading_scene())
    assert len(EventManager.listeners) == 2
    assert not any(isinstance(ctl, CombatSceneController)
                   for ctl in EventManager.listeners)

    event_utils.post_scene_change(CombatScene())
    assert len(EventManager.listeners) == 2

    assert any(isinstance(ctl, CombatSceneController)
               for ctl in EventManager.listeners)
