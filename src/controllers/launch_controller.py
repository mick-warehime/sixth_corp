from controllers.controller import Controller
from events.events_base import EventManager, NewSceneEvent, EventType
from events.events_base import Event
from events.events_base import InputEvent
from views.launch_view import LaunchView

from scenes.scenes_base import Scene


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