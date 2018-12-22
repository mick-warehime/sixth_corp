from listener import Listener
from event_manager import EventManager
from events import Event


class EventListener(Listener):

    def __init__(self, event_manager: EventManager) -> None:
        event_manager.register(self)
        self.event_manager = event_manager

    def notify(self, event: Event) -> None:
        pass
