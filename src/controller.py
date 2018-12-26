import logging

from abstract_view import View
from events import EventListener, Event
from pygame import Surface


class Controller(EventListener):

    def __init__(self, screen: Surface) -> None:
        super(Controller, self).__init__()
        self.screen = screen
        self.view: View = None
        self._active = True
        self.activate()

    def activate(self) -> None:
        logging.debug('Activating {}'.format(self))
        self._active = True

    def deactivate(self) -> None:
        logging.debug('Deactivating {}'.format(self))
        self._active = False

    def notify(self, event: Event) -> None:
        raise NotImplementedError
