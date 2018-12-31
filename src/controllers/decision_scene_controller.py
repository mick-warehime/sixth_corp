from models.conditions import IsDead
from controllers.controller import Controller
from scenes.decision_scene import DecisionScene
from views.decision_scene_view import DecisionSceneView
from events.event_utils import post_scene_change
from events.events_base import InputEvent, EventType, Event
from scenes.scene_examples import game_over
from models.world import World


class DecisionSceneController(Controller):

    def __init__(self, scene: DecisionScene) -> None:
        super().__init__()
        self._world = World()
        self._scene = scene

        options = {key_val: choice.description
                   for key_val, choice in scene.choices.items()}
        self.view = DecisionSceneView(scene.prompt, options)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self._scene.choices:
            self._scene.make_choice(input_event.key)

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
            if self._scene.is_resolved():
                resolution = self._scene.get_resolution()
                for effect in resolution.effects:
                    effect.execute()

                self.deactivate()
                if IsDead().check(self._world.player):
                    post_scene_change(game_over())
                    return
                post_scene_change(resolution.next_scene())
        elif isinstance(event, InputEvent):
            self._handle_input(event)
