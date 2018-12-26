from conditions import IsDead
from controller import Controller
from decision_scene import DecisionScene
from decision_scene_view import DecisionSceneView
from events import Event, NewSceneEvent, EventType
from events import InputEvent
from events import EventManager
from pygame import Surface

from scene_examples import game_over
from world import World


class DecisionSceneController(Controller):

    def __init__(self, screen: Surface, world: World,
                 scene: DecisionScene) -> None:
        super(DecisionSceneController, self).__init__(screen)
        self.scene = scene
        options = {key_val: choice.description
                   for key_val, choice in scene.choices.items()}
        self.view = DecisionSceneView(self.screen, scene.prompt, options)
        self.world = world

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
            if self.scene.is_resolved():
                resolution = self.scene.get_resolution()
                for effect in resolution.effects:
                    effect.execute(self.world)

                if IsDead().check(self.world.player):
                    EventManager.post(NewSceneEvent(game_over(self.world)))
                    return

                EventManager.post(
                    NewSceneEvent(resolution.next_scene(self.world)))
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self.scene.choices:
            self.scene.make_choice(input_event.key)
