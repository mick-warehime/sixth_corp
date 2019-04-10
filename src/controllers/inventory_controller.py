from controllers.controller import Controller
from events.events_base import EventTypes, EventType


class InventoryController(Controller):

    def __init__(self) -> None:
        super().__init__()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return

        if event != EventTypes.TICK:
            pass
