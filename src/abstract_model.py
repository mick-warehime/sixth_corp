from events import Event
from events import EventListener


class Model(EventListener):

    def notify(self, event: Event) -> None:
        pass
