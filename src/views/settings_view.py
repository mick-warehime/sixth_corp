from views.pygame_view import PygameView

_SETTINGS_BACKGROUND = 'src/images/background_settings.png'
_SETTINGS_OPTIONS = ('Settings!', 'X: Return')


class SettingsView(PygameView):
    def __init__(self) -> None:
        super(SettingsView, self).__init__(_SETTINGS_BACKGROUND)

    def render(self) -> None:
        super().render()
        self.render_text(_SETTINGS_OPTIONS)
