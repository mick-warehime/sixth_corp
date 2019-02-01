from typing import Tuple

from data.constants import SCREEN_SIZE

_REF_SCREEN_WIDTH = 1200
_REF_SCREEN_HEIGHT = 900

_HORIZONTAL_SCALE = SCREEN_SIZE[0] / _REF_SCREEN_WIDTH
_VERTICAL_SCALE = SCREEN_SIZE[1] / _REF_SCREEN_HEIGHT


def _rescale_lengths(scale: float,
                     *lengths: int) -> Tuple[int, ...]:
    if scale != 1:
        lengths = tuple((int(l * scale) for l in lengths))
    return lengths


def rescale_horizontal(*horizontal_lengths: int) -> Tuple[int, ...]:
    return _rescale_lengths(_HORIZONTAL_SCALE, *horizontal_lengths)


def rescale_vertical(*vertical_lengths: int) -> Tuple[int, ...]:
    return _rescale_lengths(_VERTICAL_SCALE, *vertical_lengths)
