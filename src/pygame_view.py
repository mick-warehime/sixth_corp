import pygame
from events import Event
from event_manager import EventManager
from abstract_view import View


class PygameView(View):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface) -> None:
        super(View, self).__init__(event_manager)
        self.screen = screen
        pygame.display.set_caption('Droidz')
        self.smallfont = pygame.font.Font(None, 40)

    def notify(self, event: Event) -> None:
        if event == Event.TICK:
            self.render()

    def render(self) -> None:
        raise NotImplementedError("sub classes should implement this method")
