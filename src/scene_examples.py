"""Simple decision scene examples."""
from decision_scene import DecisionScene, DecisionOption
from effects import ChangeSceneName, IncrementSceneCount
from world import World


def start_scene(world: World) -> DecisionScene:
    options = {}
    for option_key in range(4):
        scene_name = str(option_key)
        options[scene_name] = DecisionOption(scene_name,
                                             ChangeSceneName(scene_name),
                                             second_scene)

    main_text = (
        'scene {}: this is a very long description of an a scene and it '
        'includes a newline.\nwhat a compelling decision i must '
        'make.'.format(world.current_scene))
    return DecisionScene(main_text, options)


def second_scene(world: World) -> DecisionScene:
    main_text = 'Scene name is now {}. Scene count is now {}.'.format(
        world.current_scene, world.scene_count)

    options = {
        '0': DecisionOption('hahah',
                            (ChangeSceneName('hahah'), IncrementSceneCount()),
                            second_scene),
        '1': DecisionOption('hoho',
                            (ChangeSceneName('hoho'), IncrementSceneCount()),
                            second_scene)
    }
    return DecisionScene(main_text, options)
