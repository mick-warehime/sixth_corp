import pygame
from event_manager import EventManager
from pygame_view import PygameView


class LaunchView(PygameView):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface) -> None:
        super(LaunchView, self).__init__(event_manager, screen)

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        somewords = self.smallfont.render(
            'New Game! (press x)', True, (0, 255, 0))
        self.screen.blit(somewords, (250, 250))
        pygame.display.flip()
