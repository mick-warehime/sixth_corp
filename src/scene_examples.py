"""Simple decision scene examples."""
from functools import partial

from character_base import Character
from combat_scene import CombatScene
from decision_scene import DecisionScene, DecisionOption
from effects import IncrementSceneCount, IncrementPlayerAttribute, RestartWorld, \
    IncrementAttribute
from states import Attribute
from world import World


def start_scene(world: World) -> DecisionScene:
    options = {}
    for option_key in range(4):
        scene_name = str(option_key)
        options[scene_name] = DecisionOption(scene_name,
                                             IncrementSceneCount(),
                                             second_scene)

    options['5'] = DecisionOption('COMBAT!', (), example_combat_scene)

    main_text = (
        'Start scene: this is a very long description of an a scene and it '
        'includes a newline.\nwhat a compelling decision i must '
        'make.')
    return DecisionScene(main_text, options)


def second_scene(world: World) -> DecisionScene:
    main_text = (
        'Player HP: {}. Player Max HP: {}. \nScene count is now {}.'.format(
            world.player.get_attribute(Attribute.HEALTH),
            world.player.get_attribute(Attribute.MAX_HEALTH),
            world.scene_count))

    options = {
        '0': DecisionOption('Gain 1 HP',
                            (IncrementSceneCount(),
                             IncrementPlayerAttribute(Attribute.HEALTH, 1)),
                            second_scene),
        '1': DecisionOption('Lose 1 HP',
                            (IncrementSceneCount(),
                             IncrementPlayerAttribute(Attribute.HEALTH, -1)),
                            second_scene)
    }
    return DecisionScene(main_text, options)


def example_combat_scene(world: World, enemy=None) -> CombatScene:
    if enemy is None:
        enemy = Character(10)
    options = {
        '0': DecisionOption('Medium attack',
                            (IncrementAttribute(enemy, Attribute.HEALTH, -1),
                             IncrementPlayerAttribute(Attribute.HEALTH, -1)),
                            partial(example_combat_scene, enemy=enemy)),
        '1': DecisionOption('Strong attack',
                            (IncrementAttribute(enemy, Attribute.HEALTH, -3),
                             IncrementPlayerAttribute(Attribute.HEALTH, -1)),
                            partial(example_combat_scene, enemy=enemy)),
        '2': DecisionOption('Stand there',
                            (IncrementPlayerAttribute(Attribute.HEALTH, -1)),
                            partial(example_combat_scene, enemy=enemy)),
    }
    return CombatScene(enemy, options)


def game_over(world: World) -> DecisionScene:
    prompt = 'Game over. You lose.'
    options = {'0': DecisionOption('Play again', RestartWorld(), start_scene)}

    return DecisionScene(prompt, options)
