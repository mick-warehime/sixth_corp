from controller import Controller
from events import EventManager
from events import Event
from events import InputEvent
from launch_view import LaunchView
from pygame import Surface


class LaunchController(Controller):

    def __init__(self, screen: Surface) -> None:
        super(LaunchController, self).__init__(screen)
        self.view = LaunchView(self.screen)

    def handle_input(self, input_event: InputEvent) -> None:
        if input_event.key == 's':
            EventManager.post(Event.NEW_SCENE)
