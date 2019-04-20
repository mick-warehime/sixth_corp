import logging

from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import (DecisionEvent, EventManager, EventType,
                                InputEvent, BasicEvents)
from models.characters.conditions import IsDead
from models.characters.player import get_player
from models.scenes.decision_scene import DecisionScene
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scene_examples import game_over_scene


class DecisionSceneController(Controller):

    def __init__(self, scene: DecisionScene) -> None:
        super().__init__()
        self._scene = scene

    def _notify(self, event: EventType) -> None:

        if isinstance(event, InputEvent):
            # Player chooses a choice
            if event.key in self._scene.choices:
                EventManager.post(DecisionEvent(event.key, self._scene))

        elif event == BasicEvents.INVENTORY:
            if self._scene.inventory_available:
                post_scene_change(InventoryScene(self._scene))

        # handle scene resolution
        # Note: this is called upon EVERY notification event. If we were to
        # change if to elif, we would encounter errors with circular references
        # preventing listeneres in EventManager from disappearing
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
