from abstract_view import View
from events import Event
from event_manager import EventManager
from typing import List
import pygame


class PygameView(View):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface) -> None:
        super(View, self).__init__(event_manager)
        self.screen = screen
        pygame.display.set_caption('6th Corp')
        self.smallfont = pygame.font.Font(None, 40)
        self.texts: List[str] = None

    def notify(self, event: Event) -> None:
        if event == Event.TICK:
            self.render()

    def render(self) -> None:
        raise NotImplementedError("sub classes should implement this method")

    def render_text(self) -> None:
        self.screen.fill((0, 0, 0))
        offset = 0
        for text in self.texts:
            rasterized = self.smallfont.render(text, True, (0, 255, 0))
            self.screen.blit(rasterized, (250, 250 + offset))
            offset += 50
        pygame.display.flip()
