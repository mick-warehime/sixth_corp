import logging

from pygame import image
from pygame.sprite import Sprite


class BackgroundImage(Sprite):
    def __init__(self, background_image_path: str) -> None:
        super().__init__()
        logging.debug('IMAGE: Loading background: {}'.format(background_image_path))
        self.image = image.load(background_image_path)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
