import pygame
from event_manager import EventManager
from pygame_view import PygameView


class SettingsView(PygameView):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface) -> None:
        super(SettingsView, self).__init__(event_manager, screen)

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        somewords = self.smallfont.render(
            'Settings! (q to return)', True, (0, 255, 255))
        self.screen.blit(somewords, (350, 250))
        pygame.display.flip()
