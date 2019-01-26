from typing import Tuple

from data.constants import SCREEN_SIZE

_REF_SCREEN_WIDTH = 1200
_REF_SCREEN_HEIGHT = 900

_HORIZONTAL_SCALE, _VERTICAL_SCALE = SCREEN_SIZE
_HORIZONTAL_SCALE /= _REF_SCREEN_WIDTH
_VERTICAL_SCALE /= _REF_SCREEN_HEIGHT


def rescale_to_screen(horizontal: int, vertical: int) -> Tuple[int, int]:
    if _HORIZONTAL_SCALE != 1:
        horizontal *= _HORIZONTAL_SCALE

    if _VERTICAL_SCALE != 1:
        vertical *= _VERTICAL_SCALE

    return int(horizontal), int(vertical)
