import logging
from typing import Dict, List
from data import constants
from models.world import get_theme
from views.background_base import BackgroundImage
import pygame


class PygameView(object):
    screen: pygame.Surface = None
    background_image_cache: Dict[str, BackgroundImage] = {}

    def __init__(self) -> None:
        if self.screen is None:
            self._initialize_screen()

        pygame.display.set_caption('6th Corp')
        self.smallfont = pygame.font.Font(None, 40)
        self.texts: List[str] = None
        self.background_image_path = None

    def render(self) -> None:
        self.clear_screen()

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def render_text(self) -> None:
        offset = 0
        for text in self.texts:
            rasterized = self.smallfont.render(text, True, (0, 255, 0))
            self.screen.blit(rasterized, (250, 250 + offset))
            offset += 50
        pygame.display.flip()

    def _initialize_screen(self) -> None:
        self.screen = pygame.display.set_mode(constants.SCREEN_SIZE)

    def render_background_image(self) -> None:
        theme = get_theme()
        bg_path = theme.background_image_path
        if bg_path not in PygameView.background_image_cache:
            background_image = BackgroundImage(bg_path)
        else:
            background_image = PygameView.background_image_cache[bg_path]

        if bg_path != self.background_image_path:
            logging.debug(
                'Loading background for {}'.format(theme.__class__.__name__))
            self.background_image_path = bg_path

        self.screen.blit(background_image.image, background_image.rect)
