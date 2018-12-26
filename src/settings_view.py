import pygame
from pygame_view import PygameView


class SettingsView(PygameView):
    def __init__(self, screen: pygame.Surface) -> None:
        super(SettingsView, self).__init__(screen)
        self.texts = ['Settings!', 'X: Return']

    def render(self) -> None:
        self.render_text()
