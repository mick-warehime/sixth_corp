import logging
from typing import Dict

import pygame

_IMAGE_CACHE: Dict[str, pygame.Surface] = {}


def load_image(image_path: str) -> pygame.Surface:
    assert image_path is not None
    if image_path not in _IMAGE_CACHE:
        logging.debug('IMAGE: Loading: {}'.format(image_path))
        _IMAGE_CACHE[image_path] = pygame.image.load(image_path)

    return _IMAGE_CACHE[image_path]
