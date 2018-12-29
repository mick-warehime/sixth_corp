from controller import Controller
from events import EventManager, NewSceneEvent, EventType
from events import Event
from events import InputEvent
from launch_view import LaunchView

from scenes_base import Scene


class LaunchController(Controller):

    def __init__(self, start_scene: Scene) -> None:
        super(LaunchController, self).__init__()
        self.view = LaunchView()
        self._start_scene = start_scene

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
        elif isinstance(event, InputEvent) and event.key == 's':
            EventManager.post(NewSceneEvent(self._start_scene))
