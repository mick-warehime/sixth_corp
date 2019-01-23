from characters.character_position import Position
from controllers.pygame_collisions import point_collides_pos

_STACK_TOP_X = 425
_STACK_TOP_Y = 200
_STACK_WIDTH = 250
_STACK_HEIGHT = 50


def stack_position(index: int) -> Position:
    """Returns the position of the ith element in the stack."""
    x = _STACK_TOP_X
    y = _STACK_TOP_Y + index * _STACK_HEIGHT
    w = _STACK_WIDTH
    h = _STACK_HEIGHT
    return Position(x, y, w, h)


def point_collides_stack_element(index: int, px: int, py: int) -> bool:
    pos = stack_position(index)
    print(pos.x, pos.y, pos.w, pos.h, px, py)
    return point_collides_pos(px, py, pos)
