from scenes.combat_scene import CombatScene
from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from scenes.decision_scene import DecisionScene
from controllers.decision_scene_controller import DecisionSceneController
from events.events_base import EventListener, Event, NewSceneEvent, EventType
from controllers.launch_controller import LaunchController
from scenes.scene_examples import start_scene
from scenes.scenes_base import Scene
from controllers.settings_controller import SettingsController
from models.world import World


SCENE_CONTROLLERS = {DecisionScene: DecisionSceneController,
                     CombatScene: CombatSceneController}


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self, ) -> None:
        super().__init__()
        self._world = World()
        self._controller = LaunchController(start_scene(self._world))
        self._prev_controller: Controller = None

    def notify(self, event: EventType) -> None:
        if event == Event.SETTINGS:
            self._toggle_settings()
        elif isinstance(event, NewSceneEvent):
            self._set_next_scene(event.scene)

    def _set_next_scene(self, scene: Scene) -> None:
        scene_type = type(scene)
        assert scene_type in SCENE_CONTROLLERS

        controller = SCENE_CONTROLLERS[scene_type]
        self._controller = controller(self._world, scene)

    def _toggle_settings(self) -> None:
        if self._prev_controller is None:
            self._prev_controller = SettingsController()

        self._prev_controller, self._controller = (
            self._controller, self._prev_controller)

        self._controller.activate()
        self._prev_controller.deactivate()