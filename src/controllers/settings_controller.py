from controllers.controller import Controller
from events.events_base import EventType


class SettingsController(Controller):

    def __init__(self) -> None:
        super(SettingsController, self).__init__()

    def _notify(self, event: EventType) -> None:
        pass
