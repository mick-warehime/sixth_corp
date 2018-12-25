from controller import Controller
from decision_scene_option import DecisionOption
from decision_scene_view import DecisionSceneView
from events import Event
from events import InputEvent
from events import EventManager
from pygame import Surface
from typing import Dict
from world import World


class DecisionSceneController(Controller):

    def __init__(self, event_manager: EventManager, screen: Surface, world: World, main_text: str,
                 options: Dict[str, DecisionOption]) -> None:
        super(DecisionSceneController, self).__init__(event_manager, screen)
        self.view = DecisionSceneView(self.event_manager, self.screen, main_text, options)
        self.options = options
        self.world = world

    def handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self.options:
            option = self.options[input_event.key]
            option.execute(self.world)
            EventManager.post(Event.NEW_SCENE)
