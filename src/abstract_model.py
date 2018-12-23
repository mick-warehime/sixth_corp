from events import Event
from events import EventListener
from events import EventManager


class Model(EventListener):
    def __init__(self, event_manager: EventManager) -> None:
        super(Model, self).__init__(event_manager)

    def notify(self, event: Event) -> None:
        pass
