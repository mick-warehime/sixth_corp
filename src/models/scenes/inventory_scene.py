from data.constants import BackgroundImages
from models.scenes.scenes_base import Resolution, Scene


class InventoryScene(Scene):

    def __init__(self) -> None:
        self.options = ('Inventory!', 'i: Return')
        self._background_image = BackgroundImages.INVENTORY.path

    @property
    def background_image(self) -> str:
        return self._background_image

    # TODO(mick) - move settings, combat, decision scene -> model classes
    def is_resolved(self) -> bool:
        return False

    def get_resolution(self) -> Resolution:
        return None
