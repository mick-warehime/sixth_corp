from decision_scene_controller import DecisionSceneController
from decision_scene import DecisionOption, DecisionScene
from controller import Controller
from launch_controller import LaunchController
from scenes_base import Scene
from settings_controller import SettingsController
from events import EventListener, Event, NewSceneEvent
from world import World
import constants
import pygame


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self, ) -> None:
        super().__init__()
        self._world = World()
        self._screen: pygame.Surface = pygame.display.set_mode(
            constants.SCREEN_SIZE)

        self._controller = LaunchController(self._screen, self._start_scene())
        self._prev_controller: Controller = None

    def notify(self, event: Event) -> None:
        if event == Event.SETTINGS:
            self._toggle_settings()
        elif isinstance(event, NewSceneEvent):
            self._set_next_scene(event.scene)

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

    def _set_next_scene(self, scene: Scene) -> None:
        assert isinstance(scene, DecisionScene)
        self._controller = DecisionSceneController(self._screen, self._world,
                                                   scene)

    def _toggle_settings(self) -> None:
        if self._prev_controller is None:
            self._prev_controller = SettingsController(self._screen)

        self._prev_controller, self._controller = (
            self._controller, self._prev_controller)

        self._controller.activate()
        self._prev_controller.deactivate()
