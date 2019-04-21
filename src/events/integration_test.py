import os
from os.path import abspath, dirname

from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.game import Game, initialize_pygame
from events import event_utils
from events.events_base import BasicEvents, EventManager
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis import ChassisData
from models.characters.conditions import IsDead
from models.characters.mods_base import GenericMod, SlotTypes
from models.characters.player import get_player
from models.characters.states import Attributes
from models.characters.subroutine_examples import direct_damage
from models.scenes import combat_scene
from models.scenes.decision_scene import DecisionOption, DecisionScene
from models.scenes.scenes_base import BasicResolution
from views.view_manager import ViewManager

# Ensure that working directory is sixth_corp
os.chdir(dirname(dirname(dirname(abspath(__file__)))))

initialize_pygame()

# Turn off game animations
combat_scene.ANIMATION = False


# Errors in other test modules may cause the EventManager to not be empty.
def setup_module(module):
    EventManager.listeners.clear()


def _get_active_controller():
    listeners = [l for l in EventManager.listeners if isinstance(l, Controller)]
    assert len(listeners) == 1
    return listeners[0]


def test_making_choices_removes_listener():
    game = Game()  # noqa: F841

    def second_scene() -> DecisionScene:
        options = {'1': DecisionOption('third scene', combat_scene.CombatScene)}
        return DecisionScene('second scene', options)

    options_0 = {'s': DecisionOption('load next scene', second_scene)}
    scene_0 = DecisionScene('first scene', options_0)

    event_utils.post_scene_change(scene_0)
    num_listeners = len(EventManager.listeners)
    ctl = _get_active_controller()
    assert isinstance(ctl, DecisionSceneController)
    # we must remove references otherwise EventManager will keep this listener
    del ctl
    del scene_0
    event_utils.simulate_key_press('s')

    assert len(EventManager.listeners) == num_listeners

    ctl = _get_active_controller()
    assert isinstance(ctl, DecisionSceneController)
    del ctl

    event_utils.simulate_key_press('1')

    assert len(EventManager.listeners) == num_listeners
    ctl = _get_active_controller()
    assert isinstance(ctl, CombatSceneController)
    del ctl


def test_press_debug_in_decision_scene_has_no_effect():
    game = Game()
    view_manager = ViewManager()

    event_utils.post_scene_change(
        DecisionScene('dummy scene for test purposes', {}))

    assert isinstance(game.scene_machine.controller, DecisionSceneController)
    assert view_manager.current_view is not None

    EventManager.post(BasicEvents.DEBUG)
    EventManager.post(BasicEvents.TICK)


def test_combat_scene_to_decision_scene():
    game = Game()  # noqa: F841
    view_manager = ViewManager()  # noqa: F841

    # dummy decision scene to which will will transision
    def dummy_scene():
        return DecisionScene('dummy scene for testing purposes', {})

    # combat scene with 1 health enemy
    enemy = build_character(CharacterData(ChassisData(
        attribute_modifiers={Attributes.MAX_HEALTH: 1}
    )))
    scene = combat_scene.CombatScene(
        enemy, win_resolution=BasicResolution(dummy_scene))
    event_utils.post_scene_change(scene)

    assert isinstance(_get_active_controller(), CombatSceneController)

    # give player ability to fire laser
    player = get_player()
    shoot_laser = direct_damage(1, label='laser', time_to_resolve=1,
                                cpu_slots=0)
    laser_mod = GenericMod(subroutines_granted=shoot_laser,
                           valid_slots=tuple(
                               s for s in SlotTypes if s != SlotTypes.STORAGE))
    assert player.chassis.can_store(laser_mod)
    player.chassis.attempt_store(laser_mod)

    assert laser_mod in player.chassis.all_active_mods()

    for _ in range(2):
        # we must do this twice because it takes a round for the first move to
        # resolve.
        # click on enemy
        enemy_pos = scene.layout.get_rects(enemy)[0].center
        event_utils.simulate_mouse_click(*enemy_pos)

        assert enemy is scene.selected_char

        # select the fire laser ability
        laser_ind = [ind for ind, move in enumerate(scene.available_moves())
                     if move.subroutine is shoot_laser][0]
        event_utils.simulate_key_press(str(laser_ind + 1))

    # check that scene has ended
    assert IsDead().check(enemy)
    assert scene.is_resolved()

    # update the scene by waiting a tick, confirm that we've switched to a
    # Decision scene
    EventManager.post(BasicEvents.TICK)
    assert isinstance(_get_active_controller(), DecisionSceneController)
