"""Simple decision scene examples."""
from decision_scene import DecisionScene, DecisionOption
from effects import ChangeSceneName
from world import World


def start_scene(world: World) -> DecisionScene:
    options = {}
    for option_key in range(4):
        scene_name = str(option_key)
        options[scene_name] = DecisionOption(scene_name,
                                             ChangeSceneName(scene_name))

    main_text = (
        'scene {}: this is a very long description of an a scene and it '
        'includes a newline.\nwhat a compelling decision i must '
        'make.'.format(world.current_scene))
    return DecisionScene(main_text, options)
