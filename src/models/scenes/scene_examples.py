"""Simple decision scene examples."""
from enum import Enum
from functools import partial
from typing import Dict, Tuple, cast

from data.constants import BackgroundImages
from models.characters.effects import IncrementAttribute, RestartGame
from models.characters.mods_base import GenericMod, Mod, SlotTypes
from models.characters.player import get_player
from models.characters.states import Attributes, Skill
from models.characters.subroutine_examples import direct_damage
from models.scenes import combat_scene
from models.scenes.decision_scene import (DecisionOption, DecisionScene,
                                          from_transition, transition_to)
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import BasicResolution, Resolution, Scene
from models.scenes.skill_checks import Difficulty, skill_check


def loading_scene() -> DecisionScene:
    options = {
        's': DecisionOption('Start Game', swamp_scene),
        'x': DecisionOption('Settings', example_combat_scene)}
    return DecisionScene('6TH Corp', options,
                         background_image=BackgroundImages.LOADING.path,
                         inventory_available=False)


def start_scene() -> DecisionScene:
    options = {'1': DecisionOption('Go in the swamp.', swamp_scene),
               '2': DecisionOption('COMBAT!', example_combat_scene)}

    main_text = (
        'You are walking down the path to the city. You pass by a decaying sign'
        ' pointing in the direction of an overgrown path. The sign says \n'
        '"DANGER: Rogue drones in swamp".\n')
    return DecisionScene(main_text, options)


def _mini_laser() -> Tuple[Mod]:
    return GenericMod(
        subroutines_granted=direct_damage(1, 0, 1, 'Mini laser'),
        valid_slots=SlotTypes.HEAD, description='Mini laser'),


@from_transition('This transition was defined using a decorator.')
def swamp_scene() -> DecisionScene:
    main_text = ('You walk into the swamp. The foliage overhead blocks most of'
                 ' the sunlight. Flies and mosquitoes buzz near your ears. Your'
                 ' olfactory sensors detect the smell of sulfur. Ahead you see '
                 'the curving form of a rogue drone. It is currently in '
                 'hibernation mode.')

    def success() -> Scene:
        load_loot_scene = partial(InventoryScene, success, _mini_laser)
        gain_3 = IncrementAttribute(Attributes.CREDITS, 3)
        return DecisionScene(
            'After deactivating the drone, you pick up 3 credits and '
            'dismantle it.',
            {'1': DecisionOption('Loot the body.', load_loot_scene),
             '2': DecisionOption('Back to start.', loading_scene, gain_3)})

    deactivate = skill_check(
        Difficulty.VERY_EASY, success,
        transition_to(example_combat_scene,
                      'The drone awakens. Prepare to fight!'),
        Skill.STEALTH)
    options = {
        '1': DecisionOption('Continue walking.', second_scene),
        '2': DecisionOption('Attempt to deactivate the drone. (SNEAK MODERATE)',
                            deactivate),
        '3': DecisionOption('Attack the drone', example_combat_scene)}
    return DecisionScene(main_text, options)


def second_scene() -> DecisionScene:
    player = get_player()
    main_text = (
        'Player HP: {}. Player Max HP: {}.'.format(
            player.status.get_attribute(Attributes.HEALTH),
            player.status.get_attribute(Attributes.MAX_HEALTH)))

    options = {
        '0': DecisionOption('Gain 1 HP', second_scene,
                            IncrementAttribute(Attributes.HEALTH, 1)),
        '1': DecisionOption('Lose 1 HP', second_scene,
                            IncrementAttribute(Attributes.HEALTH, -1))
    }
    return DecisionScene(main_text, options)


def example_combat_scene() -> 'combat_scene.CombatScene':
    restart = transition_to(start_scene, 'Back to beginning!')

    loot_scene = partial(InventoryScene, prev_scene_loader=restart,
                         loot_mods=_mini_laser)
    victory = BasicResolution(transition_to(loot_scene,
                                            'Victory! You loot the body.'))

    return combat_scene.CombatScene(win_resolution=victory)


def game_over_scene() -> DecisionScene:
    prompt = 'Game over. You loose.'
    options = {'1': DecisionOption('Play again.', loading_scene, RestartGame())}
    return DecisionScene(prompt, options)


# Resolutions

class ResolutionTypes(Enum):
    GAME_OVER = 'game over'
    RESTART = 'restart'

    @property
    def resolution(self) -> Resolution:
        # mypy does not recognize NamedTuples subclasses with multiple base
        # classes
        return cast(Resolution, _res_type_to_res[self])


_res_type_to_res: Dict[ResolutionTypes, BasicResolution] = {
    ResolutionTypes.GAME_OVER: BasicResolution(game_over_scene),
    ResolutionTypes.RESTART: BasicResolution(start_scene)
}
