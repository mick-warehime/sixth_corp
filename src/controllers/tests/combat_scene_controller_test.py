from typing import cast

from controllers.combat_scene_controller import CombatSceneController
from controllers.controller_factory import build_controller
from events.event_utils import simulate_key_press, simulate_mouse_click
from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis import ChassisData
from models.characters.states import Attributes
from models.scenes.combat_scene import CombatScene
from util.testing_util import click_on_char, selected_char


def _create_enemy(health: int = 10) -> Character:
    char_data = CharacterData(
        ChassisData(attribute_modifiers={Attributes.MAX_HEALTH: health}))
    return build_character(data=char_data)


def _create_combat_controller(enemy) -> CombatSceneController:
    return cast(CombatSceneController, build_controller(CombatScene([enemy])))


def test_game_over():
    enemy = _create_enemy(10)
    ctl = _create_combat_controller(enemy=enemy)

    assert not ctl.scene.is_resolved()

    enemy.status.increment_attribute(Attributes.HEALTH, -10)
    assert ctl.scene.is_resolved()


def test_selected_enemy():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert selected_char(ctl.scene.layout) is None

    click_on_char(enemy, ctl.scene.layout)

    assert selected_char(ctl.scene.layout) is not None
    assert selected_char(ctl.scene.layout) == enemy

    simulate_mouse_click(-1000, -1000)
    assert selected_char(ctl.scene.layout) is None


def test_enemy_unselected_after_move():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert selected_char(ctl.scene.layout) is None

    click_on_char(enemy, ctl.scene.layout)

    assert selected_char(ctl.scene.layout) is enemy

    simulate_key_press('1')
    assert selected_char(ctl.scene.layout) is None


def test_reclick_unselects():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert selected_char(ctl.scene.layout) is None

    click_on_char(enemy, ctl.scene.layout)

    assert selected_char(ctl.scene.layout) is enemy

    click_on_char(enemy, ctl.scene.layout)
    assert selected_char(ctl.scene.layout) is None


def test_click_nothing_selects_nothing():
    enemy = _create_enemy(2)
    ctl = _create_combat_controller(enemy)
    assert selected_char(ctl.scene.layout) is None

    simulate_mouse_click(-100, -100)

    assert selected_char(ctl.scene.layout) is None
