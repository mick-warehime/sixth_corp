from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.settings_controller import SettingsController
from events.events_base import Event, EventListener, EventType, NewSceneEvent
from scenes.combat_scene import CombatScene
from scenes.decision_scene import DecisionScene
from scenes.scene_examples import loading_scene
from scenes.scenes_base import Scene

SCENE_CONTROLLERS = {DecisionScene: DecisionSceneController,
                     CombatScene: CombatSceneController}


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self, ) -> None:
        super().__init__()
        self._controller: Controller = None
        self._prev_controller: Controller = None
        self._set_next_scene(loading_scene())

    def notify(self, event: EventType) -> None:
        if event == Event.SETTINGS:
            self._toggle_settings()
        if isinstance(event, NewSceneEvent):
            self._set_next_scene(event.scene)

    def _set_next_scene(self, scene: Scene) -> None:
        scene_type = type(scene)
        assert scene_type in SCENE_CONTROLLERS

        controller = SCENE_CONTROLLERS[scene_type]
        self._controller = controller(scene)

    def _toggle_settings(self) -> None:
        if self._prev_controller is None:
            self._prev_controller = SettingsController()

        self._prev_controller, self._controller = (
            self._controller, self._prev_controller)

        self._controller.activate()
        self._prev_controller.deactivate()
