from controller import Controller
from event_manager import EventManager
from events import Event
from launch_model import LaunchModel
from launch_view import LaunchView
from pygame import Surface


class LaunchController(Controller):

    def __init__(self, event_manager: EventManager, screen: Surface) -> None:
        super(LaunchController, self).__init__(event_manager, screen)
        self.model = LaunchModel(self.event_manager)
        self.view = LaunchView(self.event_manager, self.screen)

    def handle_input(self, event: Event) -> None:
        pass
