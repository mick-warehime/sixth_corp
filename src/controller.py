from events import Event
from events import InputEvent
from event_listener import EventListener
from event_manager import EventManager
from abstract_model import Model
from abstract_view import View
from pygame import Surface


class Controller(EventListener):
    view: View = None
    model: Model = None

    def __init__(self, event_manager: EventManager, screen: Surface) -> None:
        super(Controller, self).__init__(event_manager)
        self.screen = screen

    def notify(self, event: Event) -> None:
        # handle user inputs/ changes view/model
        if isinstance(event, InputEvent):
            self.handle_input(event)

    def handle_input(self, event: Event) -> None:
        raise NotImplementedError('subclasses must implement handle_input()')
