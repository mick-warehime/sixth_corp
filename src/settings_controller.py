from controller import Controller
from events import Event, EventType
from settings_view import SettingsView


class SettingsController(Controller):

    def __init__(self) -> None:
        super(SettingsController, self).__init__()
        self.view = SettingsView()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
