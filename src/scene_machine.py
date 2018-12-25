from decision_scene_controller import DecisionSceneController
from decision_scene_option import DecisionOption
from events import EventManager
from pygame import Surface
from world import World


class SceneMachine(object):

    def __init__(self) -> None:
        pass

    def build_scene(
            self,
            world: World,
            event_manager: EventManager,
            screen: Surface) -> DecisionSceneController:
        # Builds 3 options for keys 0,1 and 2 that just point to a new scene number.
        # If the option is selected it modifies the world object.
        # The decision_scene_controller listens for key presses and if the name of the key pressed
        # matches the option_key then it executes the corresponding action.
        # Feel free to change any of this.

        options = {}
        for option_key in range(4):
            scene_name = str(option_key)
            options[scene_name] = DecisionOption(world.scene_count)
            world.scene_count += 1

        main_text = 'scene {}: this is a very long description of an a scene ' \
                    'and it includes a newline.\n' \
                    'what a compelling decision i must make.'.format(world.current_scene)

        return DecisionSceneController(event_manager, screen, world, main_text, options)
