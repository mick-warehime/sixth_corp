import logging
from typing import Optional

from controllers.controller import Controller
from controllers.controller_factory import build_controller
from events.event_utils import post_scene_change
from events.events_base import (BasicEvents, EventListener, EventType,
                                NewSceneEvent)
from models.characters.conditions import is_dead
from models.characters.player import get_player
from models.scenes.scene_examples import game_over_scene
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self) -> None:
        super().__init__()
        self._current_controller: Optional[Controller] = None

        self._current_game_scene: Optional[Scene] = None  # not SettingsScene.
        self._current_scene: Optional[Scene] = None

    def notify(self, event: EventType) -> None:

        # toggle between settings scene and game scene
        if event == BasicEvents.SETTINGS:
            new_scene: Optional[Scene] = None
            # go to temp scene
            if self._current_scene is self._current_game_scene:
                new_scene = SettingsScene()
            # go back to game scene
            elif isinstance(self._current_scene, SettingsScene):
                new_scene = self._current_game_scene

            if new_scene is not None:
                post_scene_change(new_scene)

        # Check for scene resolution:
        if event == BasicEvents.TICK:
            assert self._current_scene is not None, 'No scene loaded.'
            if self._current_scene.is_resolved():
                resolution = self._current_scene.get_resolution()
                for effect in resolution.effects:
                    effect()
                logging.debug('Scene {} resolved.'.format(self._current_scene))

                if is_dead(get_player()):
                    post_scene_change(game_over_scene())
                    return

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
        assert self._current_controller is not None, 'No controller defined.'
        return self._current_controller
