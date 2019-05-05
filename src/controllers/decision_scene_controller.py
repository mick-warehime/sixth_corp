from controllers.controller import Controller
from events.events_base import (DecisionEvent, EventManager, EventType,
                                InputEvent)
from models.scenes.decision_scene import DecisionScene


class DecisionSceneController(Controller):

    def __init__(self, scene: DecisionScene) -> None:
        super().__init__()
        self._scene = scene

    def _notify(self, event: EventType) -> None:

        if isinstance(event, InputEvent):
            # Player chooses a choice
            if event.key in self._scene.choices:
                EventManager.post(DecisionEvent(event.key, self._scene))
