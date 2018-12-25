from controller import Controller
from events import InputEvent
from settings_view import SettingsView
from pygame import Surface


class SettingsController(Controller):

    def __init__(self, screen: Surface) -> None:
        super(SettingsController, self).__init__(screen)
        self.view = SettingsView(self.screen)

    def handle_input(self, input_event: InputEvent) -> None:
        pass
