from controller import Controller
from decision_scene import DecisionOption, DecisionScene
from decision_scene_view import DecisionSceneView
from events import Event
from events import InputEvent
from events import EventManager
from pygame import Surface
from typing import Dict
from world import World


class DecisionSceneController(Controller):

    def __init__(self, screen: Surface, world: World,
                 scene: DecisionScene) -> None:
        super(DecisionSceneController, self).__init__(screen)
        self.scene = scene
        self.view = DecisionSceneView(self.screen, scene.prompt, scene.choices)
        self.world = world

    def notify(self, event: Event) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
            if self.scene.is_resolved():
                resolution = self.scene.get_resolution()
                for effect in resolution.effects:
                    effect.execute(self.world)
                EventManager.post(Event.NEW_SCENE)
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self.scene.choices:
            self.scene.make_choice(input_event.key)
