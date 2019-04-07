from models.scenes.scenes_base import Resolution, Scene


class SettingsScene(Scene):

    def __init__(self) -> None:
        self.background = 'src/data/images/background_settings.png'
        self.options = ('Settings!', 'X: Return')

    # TODO(mick) - move settings, combat, decision scene -> model classes
    def is_resolved(self) -> bool:
        return False

    def get_resolution(self) -> Resolution:
        return None
