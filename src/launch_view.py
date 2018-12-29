from pygame_view import PygameView


class LaunchView(PygameView):
    def __init__(self) -> None:
        super(LaunchView, self).__init__()
        self.texts = ['New Game!', 'X: Settings', 'S: Start Game']

    def render(self) -> None:
        self.render_text()
