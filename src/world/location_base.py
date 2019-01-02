"""Class that represents the current location (sights, sounds, flavors)."""


class Location(object):

    def __init__(self, background_image_path: str) -> None:
        self._background_image_path = background_image_path

    @property
    def background_image_path(self) -> str:
        return self._background_image_path
