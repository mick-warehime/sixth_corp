"""Simple decision scene examples."""
from characters.effects import (AcquireMod, ChangeLocation, IncrementAttribute,
                                RestartGame)
from characters.mod_examples import AmuletOfSleepiness
from characters.player import get_player
from characters.skills import Difficulty, skill_check
from characters.states import Attribute, Skill
from scenes.combat_scene import CombatScene
from scenes.decision_scene import (DecisionOption, DecisionScene,
                                   from_transition, transition_to)
from world.locations import CityLocation


def loading_scene() -> DecisionScene:
    options = {
        's': DecisionOption('Start Game', (ChangeLocation(CityLocation())),
                            swamp_scene),
        'x': DecisionOption('Settings', (), example_combat_scene)}
    return DecisionScene('6TH Corp', options)


def start_scene() -> DecisionScene:
    options = {'1': DecisionOption('Go in the swamp.', (), swamp_scene),
               '2': DecisionOption('COMBAT!', (), example_combat_scene)}

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
        Difficulty.MODERATE,
        transition_to(start_scene,
                      'You expertly sneak up on the drone and deactivate it.'
                      ' You upload its credit keys into your storage. Back to '
                      'beginning.',
                      AcquireMod(AmuletOfSleepiness())),
        transition_to(example_combat_scene,
                      'The drone awakens. Prepare to fight!'),
        Skill.STEALTH)
    options = {
        '1': DecisionOption('Continue walking.', (), second_scene),
        '2': DecisionOption(
            'Attempt to deactivate the drone. (SNEAK MODERATE)', (),
            deactivate),
        '3': DecisionOption('Attack the drone', (), example_combat_scene)}
    return DecisionScene(main_text, options)


def second_scene() -> DecisionScene:
    player = get_player()
    main_text = (
        'Player HP: {}. Player Max HP: {}.'.format(
            player.get_attribute(Attribute.HEALTH),
            player.get_attribute(Attribute.MAX_HEALTH)))

    options = {
        '0': DecisionOption('Gain 1 HP',
                            IncrementAttribute(get_player(), Attribute.HEALTH,
                                               1),
                            second_scene),
        '1': DecisionOption('Lose 1 HP',
                            IncrementAttribute(get_player(), Attribute.HEALTH,
                                               -1),
                            second_scene)
    }
    return DecisionScene(main_text, options)


def example_combat_scene() -> CombatScene:
    return CombatScene()


def game_over() -> DecisionScene:
    prompt = 'Game over. You lose.'
    options = {'1': DecisionOption('Play again.', RestartGame(), loading_scene)}
    return DecisionScene(prompt, options)
