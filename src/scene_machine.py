import pygame

from controller import Controller
from launch_controller import LaunchController
from settings_controller import SettingsController
from world import World
from scene_controller import SceneController
from events import EventManager, EventListener, Event
from pygame import Surface


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self, event_manager: EventManager, world: World,
                 screen: pygame.Surface) -> None:
        super().__init__(event_manager)
        self.world = world
        self.screen = screen

        self.controller = LaunchController(self.event_manager, self.screen)
        self.prev_controller = None

    def notify(self, event: Event) -> None:
        if event == Event.SETTINGS:
            self._toggle_settings()
        elif event == Event.NEW_SCENE:
            self._set_next_scene()

    def _set_next_scene(self) -> None:
        self._remove_controller(self.controller)
        self.controller = self.build_scene(
            self.world, self.event_manager, self.screen)

    def _remove_controller(self, controller: Controller) -> None:
        self.controller.unregister()
        del controller

    def _toggle_settings(self) -> None:
        if isinstance(self.controller, SettingsController):
            self._remove_controller(self.controller)
            self.controller = self.prev_controller
        else:
            self.prev_controller = self.controller
            self.controller = SettingsController(self.event_manager,
                                                 self.screen)

    def build_scene(
            self,
            world: World,
            event_manager: EventManager,
            screen: Surface) -> SceneController:
        next_scene_name = 'Scene: {}'.format(world.scene_count)
        world.scene_count += 1
        return SceneController(event_manager, screen, next_scene_name)
