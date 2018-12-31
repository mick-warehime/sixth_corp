from views.pygame_view import PygameView


class SettingsView(PygameView):
    def __init__(self) -> None:
        super(SettingsView, self).__init__()
        self.texts = ['Settings!', 'X: Return']

    def render(self) -> None:
        super().render()
        self.render_text()
