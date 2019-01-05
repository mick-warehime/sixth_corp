from views.pygame_view import PygameView

_SETTINGS_BACKGROUND = 'src/images/background_settings.png'


class SettingsView(PygameView):
    def __init__(self) -> None:
        super(SettingsView, self).__init__(_SETTINGS_BACKGROUND)
        self.texts = ['Settings!', 'X: Return']

    def render(self) -> None:
        super().render()
        self.render_text(self.texts)
