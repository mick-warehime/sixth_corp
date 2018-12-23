from world import World
from scene_controller import SceneController
from event_manager import EventManager
from pygame import Surface


class SceneMachine(object):

    def __init__(self) -> None:
        pass

    def build_scene(
            self,
            world: World,
            event_manager: EventManager,
            screen: Surface) -> SceneController:
        next_scene_name = 'Scene: {}'.format(world.scene_count)
        world.scene_count += 1
        return SceneController(event_manager, screen, next_scene_name)
