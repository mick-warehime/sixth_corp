from typing import List
import pygame


class PygameView(object):
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        pygame.display.set_caption('6th Corp')
        self.smallfont = pygame.font.Font(None, 40)
        self.texts: List[str] = None

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
