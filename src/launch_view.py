import pygame
from pygame_view import PygameView


class LaunchView(PygameView):
    def __init__(self, screen: pygame.Surface) -> None:
        super(LaunchView, self).__init__(screen)
        self.texts = ['New Game!', 'X: Settings', 'S: Start Game']

    def render(self) -> None:
        self.render_text()
