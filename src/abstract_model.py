from events import Event
from event_listener import EventListener
from event_manager import EventManager


class Model(EventListener):
    def __init__(self, event_manager: EventManager) -> None:
        super(Model, self).__init__(event_manager)

    def notify(self, event: Event) -> None:
        pass
