from combat_scene import CombatScene
from combat_scene_controller import CombatSceneController
from decision_scene_controller import DecisionSceneController
from decision_scene import DecisionScene
from controller import Controller
from launch_controller import LaunchController
from scene_examples import start_scene
from scenes_base import Scene
from settings_controller import SettingsController
from events import EventListener, Event, NewSceneEvent, EventType
from world import World
import constants
import pygame

SCENE_CONTROLLERS = {DecisionScene: DecisionSceneController, CombatScene: CombatSceneController}


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self, ) -> None:
        super().__init__()
        self._world = World()
        self._screen: pygame.Surface = pygame.display.set_mode(
            constants.SCREEN_SIZE)

        self._controller = LaunchController(self._screen,
                                            start_scene(self._world))
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
        self._controller = controller(self._screen, self._world, scene)

    def _toggle_settings(self) -> None:
        if self._prev_controller is None:
            self._prev_controller = SettingsController(self._screen)

        self._prev_controller, self._controller = (
            self._controller, self._prev_controller)

        self._controller.activate()
        self._prev_controller.deactivate()
