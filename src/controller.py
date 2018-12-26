from abstract_model import Model
from abstract_view import View
from events import Event
from events import InputEvent
from events import EventListener
from events import EventManager
from pygame import Surface


class Controller(EventListener):

    def __init__(self, screen: Surface) -> None:
        super(Controller, self).__init__()
        self.screen = screen
        self.view: View = None
        self.model: Model = None

    def notify(self, event: Event) -> None:
        # handle user inputs/ changes view/model
        if isinstance(event, InputEvent):
            self.handle_input(event)

    def handle_input(self, input_event: InputEvent) -> None:
        raise NotImplementedError('subclasses must implement handle_input()')

    def unregister(self) -> None:
        EventManager.unregister(self.view)
        EventManager.unregister(self.model)
        EventManager.unregister(self)
