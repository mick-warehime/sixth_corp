import os
import sys
from enum import Enum

import pygame

from controllers.inputs.keyboard import Keyboard
from controllers.scene_machine import SceneMachine
from data import constants
from events.events_base import EventTypes, EventListener, EventManager, \
    EventType, NewSceneEvent
from models.scenes.scene_examples import loading_scene


class GameState(Enum):
    SETTINGS = 1
    LOAD_SCREEN = 2


def initialize_pygame(no_UI: bool = False) -> None:
    if no_UI:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'

    pygame.mixer.pre_init(44100, -16, 4, 2048)
    pygame.init()
    pygame.font.init()


class Game(EventListener):
    """Stores sceneMachine and keyboard, handles framerate and quit event."""
    keyboard: Keyboard = None

    def __init__(self) -> None:
        super(Game, self).__init__()
        self.clock: pygame.Clock = pygame.time.Clock()

        self.keyboard = Keyboard()

        self.scene_machine = SceneMachine()

    def notify(self, event: EventType) -> None:
        if event == EventTypes.QUIT:
            pygame.quit()
            sys.exit()
        elif event == EventTypes.TICK:
            # limits the redraw speed
            self.clock.tick(constants.FRAMES_PER_SECOND)

    def run(self) -> None:

        EventManager.post(NewSceneEvent(loading_scene()))

        while True:
            EventManager.post(EventTypes.TICK)
