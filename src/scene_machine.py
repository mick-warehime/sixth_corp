from controller import Controller
from decision_scene_controller import DecisionSceneController
from decision_scene_option import DecisionOption
from launch_controller import LaunchController
from settings_controller import SettingsController
from events import EventListener, Event
from pygame import Surface
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

        self._controller = LaunchController(self._screen)
        self._prev_controller: Controller = None

    def notify(self, event: Event) -> None:
        if event == Event.SETTINGS:
            self._toggle_settings()
        elif event == Event.NEW_SCENE:
            self._set_next_scene()

    def _set_next_scene(self) -> None:
        self._controller = self._build_scene(
            self._world, self._screen)

    def _toggle_settings(self) -> None:
        if self._prev_controller is None:
            self._prev_controller = SettingsController(self._screen)

        self._prev_controller, self._controller = (
            self._controller, self._prev_controller)

        self._controller.activate()
        self._prev_controller.deactivate()

    def _build_scene(
            self,
            world: World,
            screen: Surface) -> DecisionSceneController:
        # Builds 3 options for keys 0,1 and 2 that just point to a new scene
        # number. If the option is selected it modifies the world object.
        # The decision_scene_controller listens for key presses and if the name
        # of the key pressed matches the option_key then it executes the
        # corresponding action. Feel free to change any of this.

        options = {}
        for option_key in range(4):
            scene_name = str(option_key)
            options[scene_name] = DecisionOption(world.scene_count)
            world.scene_count += 1

        main_text = (
            'scene {}: this is a very long description of an a scene and it '
            'includes a newline.\nwhat a compelling decision i must '
            'make.'.format(world.current_scene))

        return DecisionSceneController(screen, world, main_text, options)
