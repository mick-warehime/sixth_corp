from enum import Enum

from events import Event
from events import EventListener
from events import EventManager
from controller import Controller
from keyboard import Keyboard
from launch_controller import LaunchController
from settings_controller import SettingsController
from scene_machine import SceneMachine
from world import World
import constants
import pygame
import sys


class GameState(Enum):
    SETTINGS = 1
    LOAD_SCREEN = 2


# TODO(mick): add decision scene
# TODO(mick): add combat scene
# TODO(mick): create player state

class Game(EventListener):
    """Loads scenes, stores world, and handles framerate and quit event."""
    keyboard: Keyboard = None
    event_manager: EventManager = None
    controller: Controller = None
    prev_controller: Controller = None

    def __init__(self) -> None:
        self.event_manager = EventManager()
        super(Game, self).__init__(self.event_manager)
        self._initialize_pygame()

        self.clock: pygame.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode(
            constants.SCREEN_SIZE)

        self.keyboard = Keyboard(self.event_manager)

        self.scene_machine = SceneMachine()
        self.world = World()

        # Change controller to change what is shown on the screen.
        self.controller = None
        self.prev_controller = None
        self._new_game()

    def notify(self, event: Event) -> None:
        if event == Event.QUIT:
            pygame.quit()
            sys.exit()
        elif event == Event.TICK:
            # limit the redraw speed to 30 frames per second

            self.clock.tick(constants.FRAMES_PER_SECOND)
        elif event == Event.SETTINGS:
            self._toggle_settings()
        elif event == Event.NEW_SCENE:
            self._set_next_scene()

    def run(self) -> None:
        while True:
            self.event_manager.post(Event.TICK)

    def _initialize_pygame(self) -> None:
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        pygame.font.init()

    def _toggle_settings(self) -> None:
        if isinstance(self.controller, SettingsController):
            self._remove_controller(self.controller)
            self.controller = self.prev_controller
        else:
            self.prev_controller = self.controller
            self.controller = SettingsController(self.event_manager, self.screen)

    def _new_game(self) -> None:
        self.controller = LaunchController(self.event_manager, self.screen)

    def _set_next_scene(self) -> None:
        self._remove_controller(self.controller)
        self.controller = self.scene_machine.build_scene(
            self.world, self.event_manager, self.screen)

    def remove_controller(self, controller: Controller) -> None:
        controller.unregister()
        del controller
