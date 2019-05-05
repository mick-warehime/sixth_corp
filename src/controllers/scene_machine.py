import logging

from controllers.controller import Controller
from controllers.controller_factory import build_controller
from events.event_utils import post_scene_change
from events.events_base import (BasicEvents, EventListener, EventType,
                                NewSceneEvent)
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self) -> None:
        super().__init__()
        self._current_controller: Controller = None

        self._current_game_scene: Scene = None  # not inventory or settings.
        self._current_scene: Scene = None

    def notify(self, event: EventType) -> None:

        # toggle between settings scene and game scene
        if event == BasicEvents.SETTINGS:
            new_scene: Scene = None
            # go to temp scene
            if self._current_scene is self._current_game_scene:
                new_scene = SettingsScene()
            # go back to game scene
            elif isinstance(self._current_scene, SettingsScene):
                new_scene = self._current_game_scene

            if new_scene is not None:
                post_scene_change(new_scene)

        # Check for scene resolution:
        if event == BasicEvents.TICK and self._current_scene.is_resolved():
            resolution = self._current_scene.get_resolution()
            for effect in resolution.effects:
                effect()
            logging.debug('Scene {} resolved.'.format(self._current_scene))

            post_scene_change(resolution.next_scene())

        # Update scene and current controller
        if isinstance(event, NewSceneEvent):

            if not isinstance(event.scene, (SettingsScene,)):
                self._current_game_scene = event.scene
            self._current_scene = event.scene

            # The previous controller may not disappear after a new controller
            # is assigned, so we must explicitly deactivate it.
            if self._current_controller is not None:
                self._current_controller.deactivate()
            self._current_controller = build_controller(event.scene)

    @property
    def controller(self) -> Controller:
        return self._current_controller
