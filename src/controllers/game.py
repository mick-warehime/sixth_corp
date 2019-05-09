import os
import sys
from typing import Callable, Optional

import pygame

from controllers.keyboard import Keyboard
from controllers.scene_machine import SceneMachine
from data import constants
from events.events_base import (BasicEvents, EventListener, EventManager,
                                EventType, NewSceneEvent)
from models.scenes.scene_examples import loading_scene
from models.scenes.scenes_base import Scene


def initialize_pygame(no_UI: bool = False) -> None:
    if no_UI:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'

    pygame.mixer.pre_init(44100, -16, 4, 2048)
    pygame.init()
    pygame.font.init()


class Game(EventListener):
    """Stores sceneMachine and keyboard, handles framerate and quit event."""
    keyboard: Optional[Keyboard] = None

    def __init__(self) -> None:
        super(Game, self).__init__()
        self.clock: pygame.Clock = pygame.time.Clock()

        self.keyboard = Keyboard()

        self.scene_machine = SceneMachine()

    def notify(self, event: EventType) -> None:
        if event == BasicEvents.QUIT:
            pygame.quit()
            sys.exit()
        elif event == BasicEvents.TICK:
            # limits the redraw speed
            self.clock.tick(constants.FRAMES_PER_SECOND)

    def run(self, scene_loader: Callable[[], Scene] = None) -> None:

        scene = loading_scene() if scene_loader is None else scene_loader()
        EventManager.post(NewSceneEvent(scene))

        while True:
            EventManager.post(BasicEvents.TICK)
