from controllers.controller import Controller
from events.events_base import EventType


class InventoryController(Controller):

    def __init__(self) -> None:
        super().__init__()

    def _notify(self, event: EventType) -> None:
        pass
