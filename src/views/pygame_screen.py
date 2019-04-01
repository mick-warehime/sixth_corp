from abc import abstractmethod
from typing import Dict, List

import pygame
from pygame.rect import Rect

from data import constants
from views.pygame_images import load_image

Color = List[int]


class Screen(object):

    @abstractmethod
    def render_texts(
            self,
            texts: List[str],
            font_size: int,
            x: int,
            y: int,
            color: Color,
            spacing: int) -> None:
        """Adds text to the screen with a font_size, position and color."""
        pass

    @abstractmethod
    def render_text(
            self, text: str, font_size: int, x: int, y: int,
            color: Color) -> None:
        """Adds text to the screen with a font_size, position and color."""
        pass

    @abstractmethod
    def render_image(self, image_path: str, x: int, y: int, w: int,
                     h: int) -> None:
        """Adds an image to the screen at (x, y) with width, w, and height, h.
        """
        pass

    @abstractmethod
    def render_rect(self, rect: Rect, color: Color, width: int) -> None:
        """Draws a rectangle onto the current screen.

        Args:
            rect: The rectangle to be drawn. Coordinates must match absolute
                screen coordinates.
            color: Fill or boundary color.
            width: Boundary width. If zero, the rect is filled.

        """


    @abstractmethod
    def clear(self) -> None:
        """Removes everything from the screen."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Makes sure any render/clear calls have been posted to the screen."""
        pass


class _PygameScreen(Screen):
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

    def update(self) -> None:
        """Makes sure any render/clear calls have been posted to the screen."""
        pygame.display.flip()

    def render_texts(
            self,
            texts: List[str],
            font_size: int,
            x: int,
            y: int,
            color: Color,
            spacing: int) -> None:
        for text in texts:
            y += spacing
            self.render_text(text, font_size, x, y, color)

    def render_text(self, text: str, font_size: int, x: int, y: int,
                    color: Color) -> None:
        font = self._font(font_size)
        rasterized = font.render(text, True, color)
        self._screen.blit(rasterized, (x, y))

    def render_image(self, image_path: str, x: int, y: int, w: int,
                     h: int) -> None:
        image = load_image(image_path)
        rect = image.get_rect()
        rect.x = x
        rect.y = y
        if w > 0 and h > 0:
            image = pygame.transform.scale(image, (w, h))
        self._screen.blit(image, rect)

    def render_rect(self, rect: Rect, color: Color, width: int) -> None:
        pygame.draw.rect(self._screen, color, rect, width)

    def clear(self) -> None:
        self._screen.fill((0, 0, 0))


_screen = None


def get_screen() -> Screen:
    global _screen
    if _screen is None:
        _screen = _PygameScreen()
    return _screen
