from typing import cast

from controllers.combat_scene_controller import CombatSceneController
from controllers.controller_factory import build_controller
from events.event_utils import simulate_key_press, simulate_mouse_click
from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis_examples import ChassisData
from models.characters.states import Attributes
from models.scenes.combat_scene import CombatScene


def _create_enemy(health: int = 10) -> Character:
    char_data = CharacterData(
        ChassisData(attribute_modifiers={Attributes.MAX_HEALTH: health}))
    return build_character(char_data)


def _create_combat_controller(enemy) -> CombatSceneController:
    return cast(CombatSceneController, build_controller(CombatScene(enemy)))


def _click_on_char(char: Character, controller: CombatSceneController):
    rects = controller.scene.layout.get_rects(char)
    assert len(rects) == 1

    simulate_mouse_click(*rects[0].center)


def test_game_over():
    enemy = _create_enemy(10)
    ctl = _create_combat_controller(enemy=enemy)

    assert not ctl.scene.is_resolved()

    enemy.status.increment_attribute(Attributes.HEALTH, -10)
    assert ctl.scene.is_resolved()


def test_selected_enemy():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert ctl.scene.selected_char is None

    _click_on_char(enemy, ctl)

    assert ctl.scene.selected_char is not None
    assert ctl.scene.selected_char == enemy

    simulate_mouse_click(-1000, -1000)
    assert ctl.scene.selected_char is None


def test_enemy_unselected_after_move():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert ctl.scene.selected_char is None

    _click_on_char(enemy, ctl)

    assert ctl.scene.selected_char is enemy

    simulate_key_press('1')
    assert ctl.scene.selected_char is None


def test_reclick_unselects():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert ctl.scene.selected_char is None

    _click_on_char(enemy, ctl)

    assert ctl.scene.selected_char is enemy

    _click_on_char(enemy, ctl)
    assert ctl.scene.selected_char is None


def test_click_nothing_selects_nothing():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert ctl.scene.selected_char is None

    simulate_mouse_click(-100, -100)

    assert ctl.scene.selected_char is None
