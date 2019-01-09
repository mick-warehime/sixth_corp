from characters.conditions import IsDead
from characters.player import get_player
from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import Event, EventType, InputEvent
from scenes.decision_scene import DecisionScene
from scenes.scene_examples import game_over
from views.decision_scene_view import DecisionSceneView
from world.world import get_world


class DecisionSceneController(Controller):

    def __init__(self, scene: DecisionScene) -> None:
        super().__init__()
        self._world = get_world()
        self._scene = scene

        options = {key_val: choice.description
                   for key_val, choice in scene.choices.items()}
        self.view = DecisionSceneView(scene.prompt, options)
        self.view.render()

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self._scene.choices:
            self._scene.make_choice(input_event.key)

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.check_resolution()
        elif isinstance(event, InputEvent):
            self._handle_input(event)
            self.view.render()

    def check_resolution(self) -> None:
        if self._scene.is_resolved():
            resolution = self._scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()

            self.deactivate()
            if IsDead().check(get_player()):
                post_scene_change(game_over())
                return
            post_scene_change(resolution.next_scene())
