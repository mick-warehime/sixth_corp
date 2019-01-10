from typing import Iterable

import pygame
from pygame import Surface

from data import constants
from views.pygame_images import load_image


class PygameView(object):
    screen: Surface = None

    def __init__(self, background_image_path: str) -> None:
        if self.screen is None:
            self._initialize_screen()

        self._smallfont = pygame.font.Font(None, 40)
        self._background_path = background_image_path

    def _initialize_screen(self) -> None:
        pygame.display.set_caption('6th Corp')
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)

    def render(self) -> None:
        self.clear_screen()
        self.render_background(self._background_path)
        self.update_display()

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def render_text(self, texts: Iterable[str]) -> None:
        offset = 0
        for text in texts:
            rasterized = self._smallfont.render(text, True, (0, 255, 0))
            self.screen.blit(rasterized, (250, 250 + offset))
            offset += 50
        self.update_display()

    def _initialize_screen(self) -> None:
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)

    def update_display(self) -> None:
        pygame.display.flip()

    def render_background(self, image_path: str) -> None:
        self.render_image(image_path, 0, 0)

    def render_image(self, image_path: str, x: int, y: int, w: int = 0, h: int = 0) -> None:
        image = load_image(image_path)
        rect = image.get_rect()
        rect.x = x
        rect.y = y
        if w > 0 and h > 0:
            image = pygame.transform.scale(image, (w, h))
        self.screen.blit(image, rect)
        self.update_display()

    def draw_rect(self, x: int, y: int, w: int, h: int) -> None:
        pygame.draw.rect(self.screen, [250, 0, 0], pygame.rect.Rect(x, y, w, h), 2)
        self.update_display()
