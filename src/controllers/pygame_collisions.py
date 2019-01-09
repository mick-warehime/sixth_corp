from pygame.rect import Rect


def point_collides_rect(px: int, py: int, x: int, y: int, w: int, h: int) -> bool:
    return Rect(x, y, w, h).collidepoint(px, py)
