import pygame
from events import EventManager
from pygame_view import PygameView


class SettingsView(PygameView):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface) -> None:
        super(SettingsView, self).__init__(event_manager, screen)
        self.texts = ['Settings!', 'X: Return']

    def render(self) -> None:
        self.render_text()
