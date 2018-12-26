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

    def notify(self, event: Event) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
        elif isinstance(event, InputEvent) and event.key == 's':
            EventManager.post(Event.NEW_SCENE)
