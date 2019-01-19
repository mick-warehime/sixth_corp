import logging

from characters.conditions import IsDead
from characters.player import get_player
from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import (ControllerActivatedEvent, Event, EventType,
                                InputEvent)
from scenes.decision_scene import DecisionScene
from scenes.scene_examples import game_over
from views.view_factory import SceneViewType, build_scene_view


class DecisionSceneController(Controller):

    def __init__(self, scene: DecisionScene) -> None:
        super().__init__()
        self._scene = scene
        self.view = build_scene_view(SceneViewType.Decision, scene)
        self.update()

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
            self.update()
        elif isinstance(event, ControllerActivatedEvent):
            self.update()

    def check_resolution(self) -> None:
        if self._scene.is_resolved():
            resolution = self._scene.get_resolution()
            for effect in resolution.effects:
                logging.debug('Applying effect of type {}'.format(
                    effect.__class__.__name__))
                effect.execute()

            self.deactivate()
            if IsDead().check(get_player()):
                post_scene_change(game_over())
                return
            post_scene_change(resolution.next_scene())

    def update(self) -> None:
        self.view.update()
