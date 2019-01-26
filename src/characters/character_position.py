from typing import Tuple

from views.artists.drawing_utils import rescale_to_screen


class Position(object):

    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0,
                 rescale: bool = True) -> None:
        if rescale:
            x, y = rescale_to_screen(x, y)
            w, h = rescale_to_screen(w, h)

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def center(self) -> Tuple[int, int]:
        cx = int(self.x + self.w / 2)
        cy = int(self.y + self.h / 2)
        return (cx, cy)
