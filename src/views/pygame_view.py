from typing import Dict, List
from data import constants
from views.background_base import BackgroundImage
import pygame


class PygameView(object):
    screen: pygame.Surface = None
    background_image_cache: Dict[str, BackgroundImage] = {}

    def __init__(self, background_image_path: str) -> None:
        if self.screen is None:
            self._initialize_screen()

        pygame.display.set_caption('6th Corp')
        self.smallfont = pygame.font.Font(None, 40)
        self.texts: List[str] = None
        self._background_image = self.load_background(background_image_path)

    def render(self) -> None:
        self.clear_screen()
        self.render_background_image()

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
        self.screen.blit(self._background_image.image, self._background_image.rect)

    def load_background(self, image_path: str) -> BackgroundImage:
        if image_path not in PygameView.background_image_cache:
            background_image = BackgroundImage(image_path)
            PygameView.background_image_cache[image_path] = background_image
        else:
            background_image = PygameView.background_image_cache[image_path]
        return background_image
