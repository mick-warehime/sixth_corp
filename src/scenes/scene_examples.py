"""Simple decision scene examples."""
from typing import Sequence

from characters.effects import ChangeLocation, IncrementAttribute, RestartGame
from characters.player import get_player
from characters.skills import Difficulty, skill_check
from characters.states import Attributes, Skill
from scenes import combat_scene
from scenes.decision_scene import (DecisionOption, DecisionScene,
                                   from_transition, transition_to)
from scenes.scenes_base import Resolution, Scene, Effect
from world.locations import CityLocation


# Scenes

def loading_scene() -> DecisionScene:
    options = {
        's': DecisionOption('Start Game', swamp_scene,
                            [ChangeLocation(CityLocation())]),
        'x': DecisionOption('Settings', example_combat_scene)}
    return DecisionScene('6TH Corp', options)


def start_scene() -> DecisionScene:
    options = {'1': DecisionOption('Go in the swamp.', swamp_scene),
               '2': DecisionOption('COMBAT!', example_combat_scene)}

    main_text = (
        'You are walking down the path to the city. You pass by a decaying sign'
        ' pointing in the direction of an overgrown path. The sign says \n'
        '"DANGER: Rogue drones in swamp".\n')
    return DecisionScene(main_text, options)


@from_transition('This transition was defined using a decorator.')
def swamp_scene() -> DecisionScene:
    main_text = ('You walk into the swamp. The foliage overhead blocks most of'
                 ' the sunlight. Flies and mosquitoes buzz near your ears. Your'
                 ' olfactory sensors detect the smell of sulfur. Ahead you see '
                 'the curving form of a rogue drone. It is currently in '
                 'hibernation mode.')
    deactivate = skill_check(
        Difficulty.VERY_EASY,
        transition_to(start_scene,
                      'You expertly sneak up on the drone and deactivate it.'
                      ' You upload its credit 3 keys into your storage.'
                      ' Back to beginning.',
                      IncrementAttribute(get_player(), Attributes.CREDITS, 3)),
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
                            IncrementAttribute(get_player(), Attributes.HEALTH,
                                               1)),
        '1': DecisionOption('Lose 1 HP', second_scene,
                            IncrementAttribute(get_player(), Attributes.HEALTH,
                                               -1))
    }
    return DecisionScene(main_text, options)


def example_combat_scene() -> 'combat_scene.CombatScene':
    return combat_scene.CombatScene()


def game_over_scene() -> DecisionScene:
    prompt = 'Game over. You loose.'
    options = {'1': DecisionOption('Play again.', loading_scene, RestartGame())}
    return DecisionScene(prompt, options)


# Resolutions

class EndGame(Resolution):

    def next_scene(self) -> Scene:
        return game_over_scene()

    @property
    def effects(self) -> Sequence[Effect]:
        return ()


class CombatResolution(Resolution):

    @property
    def effects(self) -> Sequence[Effect]:
        return []

    def next_scene(self) -> Scene:
        return start_scene()
