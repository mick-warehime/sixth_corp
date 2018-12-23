import pygame
from event_manager import EventManager
from pygame_view import PygameView


class LaunchView(PygameView):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface) -> None:
        super(LaunchView, self).__init__(event_manager, screen)
        self.texts = ['New Game!', 'X: Settings', 'S: Start Game']

    def render(self) -> None:
        self.render_text()
