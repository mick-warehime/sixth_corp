"""Simple decision scene examples."""
from models.abilities import skill_check, Difficulty
from scenes.combat_scene import CombatScene
from scenes.decision_scene import DecisionScene, DecisionOption, transition_to, \
    from_transition
from models.effects import IncrementSceneCount, IncrementPlayerAttribute, RestartWorld
from models.states import Attribute, Ability
from models.world import World


def start_scene(world: World) -> DecisionScene:
    options = {'1': DecisionOption('Go in the swamp.',
                                   IncrementSceneCount(), swamp_scene),
               '2': DecisionOption('COMBAT!', (), example_combat_scene)}

    main_text = (
        'You are walking down the path to the city. You pass by a decaying sign '
        'pointing in the direction of an overgrown path. The sign says \n'
        '"DANGER: Trolls in swamp".\n')
    return DecisionScene(main_text, options)


@from_transition('This transition was defined using a decorator.')
def swamp_scene(world: World) -> DecisionScene:
    main_text = ('You walk into the swamp. The foliage overhead blocks most of'
                 ' the sunlight. Flies and mosquitoes buzz near your ears. The '
                 'smell of sulfur pervades. Ahead you see the curving form of a'
                 ' sleeping troll. On its neck hangs a golden amulet.')
    steal_amulet = skill_check(
        Difficulty.MODERATE,
        transition_to(start_scene, 'You expertly steal the amulet without '
                                   'waking the troll. Back to beginning.'),
        transition_to(example_combat_scene,
                      'The troll awakens. Prepare to fight!'),
        Ability.STEALTH)
    options = {
        '1': DecisionOption('Continue walking.', IncrementSceneCount(),
                            second_scene),
        '2': DecisionOption(
            'Attempt to steal the amulet. (SNEAK MODERATE)', (), steal_amulet),
        '3': DecisionOption('Attack the troll', (), example_combat_scene)}
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


def example_combat_scene(world: World) -> CombatScene:
    return CombatScene()


def game_over(world: World) -> DecisionScene:
    prompt = 'Game over. You lose.'
    options = {'1': DecisionOption('Play again.', RestartWorld(), start_scene)}
    return DecisionScene(prompt, options)