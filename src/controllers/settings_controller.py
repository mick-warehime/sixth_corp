from controllers.controller import Controller
from events.events_base import EventType


class SettingsController(Controller):

    def __init__(self) -> None:
        super(SettingsController, self).__init__()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
