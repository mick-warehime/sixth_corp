from enum import Enum

from events.events_base import Event, EventType
from events.events_base import EventListener
from events.events_base import EventManager
from inputs.keyboard import Keyboard
from scenes.scene_machine import SceneMachine
from data import constants
import pygame
import sys


class GameState(Enum):
    SETTINGS = 1
    LOAD_SCREEN = 2


# TODO(mick): add decision scene
# TODO(mick): add combat scene
# TODO(mick): create player state

class Game(EventListener):
    """Stores sceneMachine and keyboard, handles framerate and quit event."""
    keyboard: Keyboard = None

    def __init__(self) -> None:
        super(Game, self).__init__()
        self._initialize_pygame()

        self.clock: pygame.Clock = pygame.time.Clock()

        self.keyboard = Keyboard()

        self.scene_machine = SceneMachine()

    def notify(self, event: EventType) -> None:
        if event == Event.QUIT:
            pygame.quit()
            sys.exit()
        elif event == Event.TICK:
            # limits the redraw speed
            self.clock.tick(constants.FRAMES_PER_SECOND)

    def run(self) -> None:
        while True:
            EventManager.post(Event.TICK)

    def _initialize_pygame(self) -> None:
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()
        pygame.font.init()