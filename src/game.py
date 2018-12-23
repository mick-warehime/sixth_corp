from enum import Enum
from events import Event
from event_listener import EventListener
from event_manager import EventManager
from controller import Controller
from keyboard import Keyboard
from launch_controller import LaunchController
from settings_controller import SettingsController
import constants
import pygame
import sys


class GameState(Enum):
    SETTINGS = 1
    LOAD_SCREEN = 2


# TODO(mick): add scene_machine(world) -> scene
# TODO(mick): add game state (decision scene)
# TODO(mick): add decision scene
# TODO(mick): add game state (combat scene)
# TODO(mick): add combat scene
# TODO(mick): create player state
# TODO(mick): create world state


class Game(EventListener):
    keyboard: Keyboard = None
    event_manager: EventManager = None
    controller: Controller = None

    def __init__(self) -> None:
        self.event_manager = EventManager()
        super(Game, self).__init__(self.event_manager)
        self.inialize_pygame()

        self.clock: pygame.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode(
            constants.SCREEN_SIZE)

        self.keyboard = Keyboard(self.event_manager)

        self.controller = LaunchController(self.event_manager, self.screen)

    def notify(self, event: Event) -> None:
        if event == Event.QUIT:
            pygame.quit()
            sys.exit()
        elif event == Event.TICK:
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)
        elif event == Event.SETTINGS:
            self.toggle_settigns()

    def run(self) -> None:
        while True:
            self.event_manager.post(Event.TICK)

    def inialize_pygame(self) -> None:
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        pygame.font.init()

    def toggle_settigns(self) -> None:
        if isinstance(self.controller, SettingsController):
            self.controller = LaunchController(self.event_manager, self.screen)
        else:
            self.controller = SettingsController(self.event_manager, self.screen)
