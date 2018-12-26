import logging

from abstract_model import Model
from abstract_view import View
from events import Event
from events import InputEvent
from events import EventListener
from pygame import Surface


class Controller(EventListener):

    def __init__(self, screen: Surface) -> None:
        super(Controller, self).__init__()
        self.screen = screen
        self.view: View = None
        self.model: Model = None
        self._active = True
        self.activate()

    def activate(self):
        logging.debug('Activating {}'.format(self))
        self._active = True

    def deactivate(self):
        logging.debug('Deactivating {}'.format(self))
        self._active = False

    def notify(self, event: Event) -> None:
        # handle user inputs/ changes view/model
        if not self._active:
            return
        if isinstance(event, InputEvent) and self._active:
            self.handle_input(event)

    def handle_input(self, input_event: InputEvent) -> None:
        raise NotImplementedError('subclasses must implement handle_input()')
