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
        options = {}
        for i in range(3):
            scene_name = '{}'.format(i)
            options[scene_name] = DecisionOption(world.scene_count)
            world.scene_count += 1

        main_text = 'scene {}: select next scene'.format(world.current_scene)

        return DecisionSceneController(event_manager, screen, world, main_text, options)
