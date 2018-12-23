from controller import Controller
from events import Event
from events import InputEvent
from events import EventManager
from pygame import Surface
from scene_model import SceneModel
from scene_view import SceneView


class SceneController(Controller):

    def __init__(self, event_manager: EventManager, screen: Surface, scene_name: str) -> None:
        super(SceneController, self).__init__(event_manager, screen)
        self.model = SceneModel(self.event_manager)
        self.view = SceneView(self.event_manager, self.screen, scene_name)

    def handle_input(self, input_event: InputEvent) -> None:
        if input_event.key == 'n':
            self.event_manager.post(Event.NEW_SCENE)
