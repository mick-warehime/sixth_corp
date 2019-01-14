from controllers.controller import Controller
from events.events_base import Event, EventType
from views.settings_view import SettingsView


class SettingsController(Controller):

    def __init__(self) -> None:
        super(SettingsController, self).__init__()
        self.view = SettingsView()
        self.update()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event != Event.TICK:
            self.update()

    def update(self) -> None:
        self.view.render()
