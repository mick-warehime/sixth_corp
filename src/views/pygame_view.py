from typing import Dict, Iterable

import pygame

from data import constants
from views.background_base import BackgroundImage


class PygameView(object):
    screen: pygame.Surface = None
    background_image_cache: Dict[str, BackgroundImage] = {}

    def __init__(self, background_image_path: str) -> None:
        if self.screen is None:
            self._initialize_screen()

        pygame.display.set_caption('6th Corp')
        self.smallfont = pygame.font.Font(None, 40)
        self._background_image = self._load_background(background_image_path)

    def _initialize_screen(self) -> None:
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)

    def _load_background(self, image_path: str) -> BackgroundImage:
        if image_path not in PygameView.background_image_cache:
            background_image = BackgroundImage(image_path)
            PygameView.background_image_cache[image_path] = background_image
        else:
            background_image = PygameView.background_image_cache[image_path]
        return background_image

    def render(self) -> None:
        self.clear_screen()
        self.render_background_image()

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def render_text(self, texts: Iterable[str]) -> None:
        offset = 0
        for text in texts:
            rasterized = self.smallfont.render(text, True, (0, 255, 0))
            self.screen.blit(rasterized, (250, 250 + offset))
            offset += 50
        pygame.display.flip()

    def render_background_image(self) -> None:
        self.screen.blit(self._background_image.image,
                         self._background_image.rect)
