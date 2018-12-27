import logging

from events import EventListener, EventType
from pygame import Surface

from pygame_view import PygameView


class Controller(EventListener):

    def __init__(self, screen: Surface) -> None:
        super(Controller, self).__init__()
        self.screen = screen
        self.view: PygameView = None
        self._active = True
        self.activate()

    def activate(self) -> None:
        logging.debug('Activating {}'.format(self))
        self._active = True

    def deactivate(self) -> None:
        logging.debug('Deactivating {}'.format(self))
        self._active = False

    def notify(self, event: EventType) -> None:
        raise NotImplementedError
