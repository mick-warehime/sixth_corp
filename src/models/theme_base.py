"""Class that represents the theme (sights, sounds, flavors) of the world."""


class Theme(object):

    def __init__(self, background_image_path: str) -> None:
        self._background_image_path = background_image_path

    @property
    def background_image_path(self) -> str:
        return self._background_image_path
