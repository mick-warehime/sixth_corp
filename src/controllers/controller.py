import logging

from events.events_base import EventListener, EventType
from views.pygame_view import PygameView


class Controller(EventListener):

    def __init__(self) -> None:
        super(Controller, self).__init__()
        self._active = True
        self.activate()

    def activate(self) -> None:
        logging.debug('Activating a {}'.format(self.__class__.__name__))
        self._active = True

    def deactivate(self) -> None:
        logging.debug('Deactivating a {}'.format(self.__class__.__name__))
        self._active = False

    def notify(self, event: EventType) -> None:
        raise NotImplementedError
