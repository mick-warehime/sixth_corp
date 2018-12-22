from controller import Controller
from events import Event
from event_manager import EventManager
from settings_model import SettingsModel
from settings_view import SettingsView
from pygame import Surface


class SettingsController(Controller):

    def __init__(self, event_manager: EventManager, screen: Surface) -> None:
        super(SettingsController, self).__init__(event_manager, screen)
        self.model = SettingsModel(self.event_manager)
        self.view = SettingsView(self.event_manager, self.screen)

    def handle_input(self, event: Event) -> None:
        pass
