from abc import abstractmethod
from typing import List

Color = List[int]


class Screen(object):

    @abstractmethod
    def render_texts(self, texts: List[str], font_size: int, x: int, y: int, color: Color) -> None:
        """Adds text to the screen with a font_size, position and color."""
        pass

    @abstractmethod
    def render_text(self, text: str, font_size: int, x: int, y: int, color: Color) -> None:
        """Adds text to the screen with a font_size, position and color."""
        pass

    @abstractmethod
    def render_image(self, image_path: str, x: int, y: int, w: int = 0, h: int = 0) -> None:
        """Adds an image to the screen at (x, y) with width, w, and height, h."""
        pass

    @abstractmethod
    def render_rect(self, x: int, y: int, w: int, h: int, color: Color, width: int) -> None:
        """Draws a rectangle onto the current screen."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Removes everything from the screen."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Makes sure any render/clear calls have been posted to the screen."""
        pass
