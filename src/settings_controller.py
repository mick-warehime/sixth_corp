from controller import Controller
from events import InputEvent
from events import EventManager
from settings_view import SettingsView
from pygame import Surface


class SettingsController(Controller):

    def __init__(self, event_manager: EventManager, screen: Surface) -> None:
        super(SettingsController, self).__init__(event_manager, screen)
        self.view = SettingsView(self.event_manager, self.screen)

    def handle_input(self, input_event: InputEvent) -> None:
        pass
