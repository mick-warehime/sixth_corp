from pygame.rect import Rect


def point_collides_rect(px: int, py: int, x: int, y: int, w: int,
                        h: int) -> bool:
    return Rect(x, y, w, h).collidepoint(px, py)


def point_collides_pos(px: int, py: int, pos: Rect) -> bool:
    return point_collides_rect(px, py, pos.x, pos.y, pos.w, pos.h)
