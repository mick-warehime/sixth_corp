from typing import Dict, Iterable, List

import pygame
from pygame import Surface

from characters.player import get_player
from characters.states import Attribute
from data import constants
from views.pygame_images import load_image

DARK_GRAY = [50, 50, 50]
RED = [255, 0, 0]
GREEN = [0, 255, 0]


class PygameView(object):
    screen: Surface = None

    def __init__(self, background_image_path: str) -> None:
        if self.screen is None:
            self._initialize_screen()
        self._background_path = background_image_path
        self._fonts: Dict[int, pygame.font.Font] = {}

    def font(self, size: int) -> pygame.font.Font:
        if size not in self._fonts:
            font = pygame.font.Font(None, size)
            self._fonts[size] = font
        else:
            font = self._fonts[size]
        return font

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
        x = 250
        for text in texts:
            y = 250 + offset
            self.render_font(text, 40, x, y, GREEN)
            offset += 50
        self.update_display()

    def render_font(self, text: str, size: int, x: int, y: int, color: List[int]) -> None:
        font = self.font(size)
        rasterized = font.render(text, True, color)
        self.screen.blit(rasterized, (x, y))

    def update_display(self) -> None:
        pygame.display.flip()

    def render_background(self, image_path: str) -> None:
        self.render_image(image_path, 0, 0)
        self.render_overlay()

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
        pygame.draw.rect(self.screen, RED, pygame.rect.Rect(x, y, w, h), 2)
        self.update_display()

    def render_overlay(self) -> None:

        # draw gray background
        height = 40
        width = constants.SCREEN_SIZE[0]
        pygame.draw.rect(self.screen, DARK_GRAY, pygame.rect.Rect(0, 0, width, height))

        # draw health
        player = get_player()
        health = player.get_attribute(Attribute.HEALTH)
        max_health = player.get_attribute(Attribute.MAX_HEALTH)
        health_text = 'Health: {} / {}'.format(health, max_health)
        x_health = int(width / 2 - 300)
        y_health = int(height / 2 - 5)
        self.render_font(health_text, 21, x_health, y_health, RED)
