import logging

from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import EventType, EventTypes, InputEvent
from models.characters.conditions import IsDead
from models.characters.player import get_player
from models.scenes.decision_scene import DecisionScene
from models.scenes.scene_examples import game_over_scene


class DecisionSceneController(Controller):

    def __init__(self, scene: DecisionScene) -> None:
        super().__init__()
        self._scene = scene

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self._scene.choices:
            self._scene.make_choice(input_event.key)

    def notify(self, event: EventType) -> None:
        if not self._active:
            return

        if event == EventTypes.TICK:
            self.check_resolution()
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def check_resolution(self) -> None:
        if self._scene.is_resolved():
            resolution = self._scene.get_resolution()
            for effect in resolution.effects:
                logging.debug('Applying effect of type {}'.format(
                    effect.__class__.__name__))
                effect.execute()

            self.deactivate()
            if IsDead().check(get_player()):
                post_scene_change(game_over_scene())
                return
            post_scene_change(resolution.next_scene())
