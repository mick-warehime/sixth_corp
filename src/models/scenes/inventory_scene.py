from models.scenes.scenes_base import Resolution, Scene


class InventoryScene(Scene):

    def __init__(self) -> None:
        self.options = ('Inventory!', 'i: Return')

    # TODO(mick) - move settings, combat, decision scene -> model classes
    def is_resolved(self) -> bool:
        return False

    def get_resolution(self) -> Resolution:
        return None
