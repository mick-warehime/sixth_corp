from typing import Dict, List

import pygame

from data import constants
from views.pygame_images import load_image
from views.screen_base import Color, Screen


class PygameScreen(Screen):
    _screen: pygame.Surface = None

    def __init__(self) -> None:
        if self._screen is None:
            self._initialize_screen()
        self._fonts: Dict[int, pygame.font.Font] = {}

    def _font(self, size: int) -> pygame.font.Font:
        if size not in self._fonts:
            font = pygame.font.Font(None, size)
            self._fonts[size] = font
        else:
            font = self._fonts[size]
        return font

    def _initialize_screen(self) -> None:
        pygame.display.set_caption('6th Corp')
        self._screen = pygame.display.set_mode(constants.SCREEN_SIZE)

    def _update(self) -> None:
        pygame.display.flip()

    def render_texts(
            self,
            texts: List[str],
            font_size: int,
            x: int,
            y: int,
            color: Color,
            spacing: int = 50) -> None:
        for text in texts:
            y += spacing
            self.render_text(text, font_size, x, y, color)
        self._update()

    def render_text(self, text: str, font_size: int, x: int, y: int, color: Color) -> None:
        font = self._font(font_size)
        rasterized = font.render(text, True, color)
        self._screen.blit(rasterized, (x, y))
        self._update()

    def render_image(self, image_path: str, x: int, y: int, w: int = 0, h: int = 0) -> None:
        image = load_image(image_path)
        rect = image.get_rect()
        rect.x = x
        rect.y = y
        if w > 0 and h > 0:
            image = pygame.transform.scale(image, (w, h))
        self._screen.blit(image, rect)
        self._update()

    def render_rect(self, x: int, y: int, w: int, h: int, color: Color, width: int = 0) -> None:
        pygame.draw.rect(self._screen, color, pygame.rect.Rect(x, y, w, h), width)
        self._update()

    def clear(self) -> None:
        self._screen.fill((0, 0, 0))
        self._update()
