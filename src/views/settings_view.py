from views.pygame_view import PygameView


class SettingsView(PygameView):
    def __init__(self) -> None:
        super(SettingsView, self).__init__()
        self.texts = ['Settings!', 'X: Return']

    def render(self) -> None:
        self.render_text()
