import os
from collections import defaultdict
from functools import partial
from os.path import abspath, dirname
from typing import Iterable, List, Tuple

from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.game import Game, initialize_pygame
from controllers.inventory_controller import InventoryController
from data.keybindings import Keybindings
from events import event_utils
from events.events_base import BasicEvents, EventManager
from models.characters.character_impl import build_character
from models.characters.chassis import Chassis
from models.characters.conditions import is_dead
from models.characters.mods_base import Mod, SlotTypes, build_mod
from models.characters.player import get_player, reset_player
from models.characters.states import Attributes
from models.characters.subroutine_examples import direct_damage
from models.scenes import combat_scene
from models.scenes.decision_scene import DecisionOption, DecisionScene
from models.scenes.inventory_scene import (InventoryScene, SlotHeaderInfo,
                                           SlotRowInfo)
from models.scenes.scenes_base import BasicResolution, Scene
from util.testing_util import click_on_char, selected_char
from views.view_manager import ViewManager


# Errors in other test modules may cause the EventManager to not be empty.
def setup_module(module):
    # Ensure that working directory is sixth_corp
    os.chdir(dirname(dirname(dirname(dirname(abspath(__file__))))))
    # Turn off game animations
    combat_scene.ANIMATION = False

    initialize_pygame(no_UI=True)

    # Tests in other modules may change the bindings.
    Keybindings().load()

    EventManager.listeners.clear()


def teardown_module(module):
    EventManager.listeners.clear()
    reset_player()


def _get_active_controller():
    listeners = [l for l in EventManager.listeners if isinstance(l, Controller)]
    assert len(listeners) == 1
    return listeners[0]


def test_making_choices_removes_listener():
    game = Game()  # noqa: F841

    # scene_0 (Decision) -> combat scene

    options_0 = {
        's': DecisionOption('load next scene', combat_scene.CombatScene)}
    scene_0 = DecisionScene('first scene', options_0)

    event_utils.post_scene_change(scene_0)
    ctl = _get_active_controller()
    assert isinstance(ctl, DecisionSceneController)
    # we must remove references otherwise EventManager will keep this listener
    del ctl
    del scene_0
    event_utils.simulate_key_press('s')

    # The scene machine only changes scenes on a tick
    EventManager.post(BasicEvents.TICK)

    assert not any(isinstance(l, DecisionScene) for l in EventManager.listeners)
    assert not any(isinstance(l, DecisionSceneController)
                   for l in EventManager.listeners)

    ctl = _get_active_controller()
    assert isinstance(ctl, CombatSceneController)
    assert any(isinstance(l, combat_scene.CombatScene)
               for l in EventManager.listeners)


def test_press_debug_in_decision_scene_has_no_effect():
    game = Game()
    view_manager = ViewManager()

    event_utils.post_scene_change(
        DecisionScene('dummy scene for test purposes', {}))

    assert isinstance(game.scene_machine.controller, DecisionSceneController)
    assert view_manager.current_view is not None

    EventManager.post(BasicEvents.DEBUG)
    EventManager.post(BasicEvents.TICK)


def _one_health_enemy():
    chassis = Chassis({},
                      build_mod(attribute_modifiers={Attributes.MAX_HEALTH: 1}))
    return build_character(chassis)


def test_combat_scene_to_decision_scene():
    game = Game()  # noqa: F841
    view_manager = ViewManager()  # noqa: F841

    # dummy decision scene to which will will transision
    def dummy_scene():
        return DecisionScene('dummy scene for testing purposes', {})

    # combat scene with two 1 health enemies
    enemies = [_one_health_enemy() for _ in range(2)]
    scene = combat_scene.CombatScene(
        enemies, win_resolution=BasicResolution(dummy_scene))
    event_utils.post_scene_change(scene)

    assert isinstance(_get_active_controller(), CombatSceneController)

    # Start with player holding nothing
    player = get_player()
    [player.chassis.remove_mod(mod) for mod in player.chassis.all_mods()]
    assert len(list(player.chassis.all_mods())) == 1  # Base mod only

    # give player ability to fire laser

    shoot_laser = direct_damage(1, label='laser', time_to_resolve=0,
                                cpu_slots=0)
    laser_mod = build_mod(subroutines_granted=shoot_laser,
                          valid_slots=tuple(
                              s for s in SlotTypes if s != SlotTypes.STORAGE))
    assert player.chassis.can_store(laser_mod)
    player.chassis.attempt_store(laser_mod)
    assert laser_mod in player.chassis.all_active_mods()

    # Kill each enemy
    for enemy in enemies:
        # click enemy
        click_on_char(enemy, scene.layout)

        assert enemy is selected_char(scene.layout)

        # select the fire laser ability
        laser_ind = [ind for ind, move in enumerate(scene.available_moves())
                     if move.subroutine is shoot_laser][0]
        event_utils.simulate_key_press(str(laser_ind + 1))
        assert is_dead(enemy)

    # check that scene has ended
    assert scene.is_resolved()

    # update the scene by waiting a tick, confirm that we've switched to a
    # Decision scene
    EventManager.post(BasicEvents.TICK)
    assert isinstance(_get_active_controller(), DecisionSceneController)


def _typical_mods(locations: Iterable[SlotTypes]) -> List[Mod]:
    # Loot on the ground
    out = []
    counts = defaultdict(lambda: 0)
    for loc in locations:
        counts[loc] += 1
        description = '{} mod {}'.format(loc.value, counts[loc])
        out.append(build_mod(valid_slots=loc, description=description))

    return out


def _get_current_scene() -> Scene:
    listeners = [l for l in EventManager.listeners if isinstance(l, Scene)]
    assert len(listeners) == 1
    return listeners[0]


def _slot_header_position(slot: SlotTypes, scene: InventoryScene
                          ) -> Tuple[int, int]:
    chassis = get_player().chassis

    capacity = chassis.slot_capacities[slot]
    mods = chassis.mods_in_slot(slot)
    header = SlotHeaderInfo(slot, capacity, mods)

    rects = scene.layout.get_rects(header)
    assert len(rects) == 1

    return rects[0].center


def _mod_slot_position(mod: Mod, scene: InventoryScene) -> Tuple[int, int]:
    rects = scene.layout.get_rects(SlotRowInfo(mod, False))
    if not rects:
        rects = scene.layout.get_rects(SlotRowInfo(mod, True))

    assert len(rects) == 1
    return rects[0].center


def test_inventory_scene_control_flow():
    game = Game()  # noqa: F841
    view_manager = ViewManager()  # noqa: F841

    # Start with player holding nothing
    chassis = get_player().chassis

    [chassis.remove_mod(mod) for mod in chassis.all_mods()]
    assert len(list(chassis.all_mods())) == 1  # Base mod only

    # Setup start scene that loads the loot scene
    mod_locs = [SlotTypes.HEAD, SlotTypes.HEAD, SlotTypes.CHEST, SlotTypes.LEGS]
    ground_mods = _typical_mods(mod_locs)

    def start_scene() -> DecisionScene:
        loot_scene = partial(InventoryScene, start_scene, lambda: ground_mods)
        return DecisionScene('dummy scene for testing purposes',
                             {'1': DecisionOption('Loot', loot_scene)})

    # Load loot scene
    event_utils.post_scene_change(start_scene())
    event_utils.simulate_key_press('1')
    # The scene machine only changes scenes during a game tick
    EventManager.post(BasicEvents.TICK)

    assert isinstance(_get_active_controller(), InventoryController)
    inv_scene = _get_current_scene()
    assert isinstance(inv_scene, InventoryScene)

    # Player selectes head 1 and moves it to head slot
    head_mod_1 = ground_mods[0]
    event_utils.simulate_mouse_click(*_mod_slot_position(head_mod_1, inv_scene))

    assert head_mod_1 is inv_scene.selected_mod

    head_slot_position = _slot_header_position(SlotTypes.HEAD, inv_scene)
    event_utils.simulate_mouse_click(*(head_slot_position))

    assert inv_scene.selected_mod is None
    assert head_mod_1 in chassis.all_mods()

    # Player selects head_mod_2 and tries to move it to head slot, but it is
    # full so it remains on the ground.
    assert chassis.slot_capacities[SlotTypes.HEAD] == 1
    head_mod_2 = ground_mods[1]

    head_2_slot_pos = _mod_slot_position(head_mod_2, inv_scene)
    event_utils.simulate_mouse_click(*head_2_slot_pos)

    assert head_mod_2 is inv_scene.selected_mod

    head_slot_position = _slot_header_position(SlotTypes.HEAD, inv_scene)
    event_utils.simulate_mouse_click(*(head_slot_position))

    assert inv_scene.selected_mod is None
    assert head_mod_2 not in chassis.all_mods()
    assert head_2_slot_pos == _mod_slot_position(head_mod_2, inv_scene)

    # Player moves leg mod to storage
    leg_mod = ground_mods[3]
    assert leg_mod not in chassis.all_mods()

    event_utils.simulate_mouse_click(*_mod_slot_position(leg_mod, inv_scene))
    assert leg_mod is inv_scene.selected_mod

    storage_slot_pos = _slot_header_position(SlotTypes.STORAGE, inv_scene)
    event_utils.simulate_mouse_click(*storage_slot_pos)

    assert inv_scene.selected_mod is None
    assert leg_mod in chassis.all_mods()
    assert leg_mod in chassis.mods_in_slot(SlotTypes.STORAGE)

    # Player tries to move chest mod to arms slot, so nothing happens
    chest_mod = ground_mods[2]
    assert SlotTypes.CHEST in chest_mod.valid_slots()
    assert chest_mod not in chassis.all_mods()

    event_utils.simulate_mouse_click(*_mod_slot_position(chest_mod, inv_scene))

    assert inv_scene.selected_mod is chest_mod

    arms_slot_pos = _slot_header_position(SlotTypes.ARMS, inv_scene)
    event_utils.simulate_mouse_click(*arms_slot_pos)

    assert inv_scene.selected_mod is None
    assert chest_mod not in chassis.all_mods()
