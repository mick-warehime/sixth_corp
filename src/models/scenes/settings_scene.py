from data.constants import BackgroundImages
from models.scenes.scenes_base import Resolution, Scene


class SettingsScene(Scene):

    @property
    def background_image(self) -> str:
        return self._background_image

    def __init__(self) -> None:
        self.options = ('Settings!', 'X: Return')
        self._background_image = BackgroundImages.SETTINGS.path

    # TODO(mick) - move settings, combat, decision scene -> model classes
    def is_resolved(self) -> bool:
        return False

    def get_resolution(self) -> Resolution:
        return None  # type: ignore
