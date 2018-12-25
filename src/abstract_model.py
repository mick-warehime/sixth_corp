from events import Event
from events import EventListener
from events import EventManager


class Model(EventListener):

    def notify(self, event: Event) -> None:
        pass
