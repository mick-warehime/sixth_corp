from pygame.rect import Rect

from views.artists.drawing_utils import rescale_horizontal, rescale_vertical

_STACK_TOP_X = 425
_STACK_TOP_Y = 200
_STACK_WIDTH = 250
_STACK_HEIGHT = 50


def stack_rect(index: int) -> Rect:
    """Returns the position of the ith element in the stack."""
    x = _STACK_TOP_X
    y = _STACK_TOP_Y + index * _STACK_HEIGHT
    w = _STACK_WIDTH
    h = _STACK_HEIGHT

    x, w = rescale_horizontal(x, w)
    y, h = rescale_vertical(y, h)

    return Rect(x, y, w, h)
