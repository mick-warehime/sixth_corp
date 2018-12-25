from enum import Enum

from events import Event
from events import EventListener
from events import EventManager
from controller import Controller
from keyboard import Keyboard
from scene_machine import SceneMachine
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
    """Stores sceneMachine and keyboard, andles framerate and quit event."""
    keyboard: Keyboard = None
    event_manager: EventManager = None
    controller: Controller = None
    prev_controller: Controller = None

    def __init__(self) -> None:
        self.event_manager = EventManager()
        super(Game, self).__init__(self.event_manager)
        self._initialize_pygame()

        self.clock: pygame.Clock = pygame.time.Clock()

        self.keyboard = Keyboard(self.event_manager)

        self.scene_machine = SceneMachine(self.event_manager)

    def notify(self, event: Event) -> None:
        if event == Event.QUIT:
            pygame.quit()
            sys.exit()
        elif event == Event.TICK:
            # limit the redraw speed to 30 frames per second

            self.clock.tick(constants.FRAMES_PER_SECOND)

    def run(self) -> None:
        while True:
            self.event_manager.post(Event.TICK)

    def _initialize_pygame(self) -> None:
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        pygame.font.init()
