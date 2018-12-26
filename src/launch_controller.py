from controller import Controller
from decision_scene import DecisionScene, DecisionOption
from decision_scene_controller import DecisionSceneController
from events import EventManager, NewSceneEvent
from events import Event
from events import InputEvent
from launch_view import LaunchView
from pygame import Surface

from world import World


class LaunchController(Controller):

    def __init__(self, screen: Surface, world: World) -> None:
        super(LaunchController, self).__init__(screen)
        self.view = LaunchView(self.screen)
        self._world = world

    def notify(self, event: Event) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
        elif isinstance(event, InputEvent) and event.key == 's':
            EventManager.post(NewSceneEvent(self._start_scene()))

    def _start_scene(self) -> DecisionScene:
        options = {}
        for option_key in range(4):
            scene_name = str(option_key)
            options[scene_name] = DecisionOption(self._world.scene_count)
            self._world.scene_count += 1

        main_text = (
            'scene {}: this is a very long description of an a scene and it '
            'includes a newline.\nwhat a compelling decision i must '
            'make.'.format(self._world.current_scene))
        return DecisionScene(main_text, options)
