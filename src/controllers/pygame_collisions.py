from pygame.rect import Rect
from characters.character_position import Position


def point_collides_rect(px: int, py: int, x: int, y: int, w: int, h: int) -> bool:
    return Rect(x, y, w, h).collidepoint(px, py)


def point_collides_pos(px: int, py: int, pos: Position) -> bool:
    return point_collides_rect(px, py, pos.x, pos.y, pos.w, pos.h)
