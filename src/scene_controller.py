from abc import ABCMeta, abstractmethod

from pygame import Surface

from conditions import IsDead
from controller import Controller
from events import EventType, Event, EventManager, NewSceneEvent, InputEvent
from scene_examples import game_over
from scenes_base import Scene
from world import World


class SceneController(Controller, metaclass=ABCMeta):
    def __init__(self, screen: Surface, world: World, scene: Scene):
        super().__init__(screen)
        self.world = world
        self.scene = scene

    @abstractmethod
    def _handle_input(self, input_event: EventType)->None:
        pass

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
            if self.scene.is_resolved():
                resolution = self.scene.get_resolution()
                for effect in resolution.effects:
                    effect.execute(self.world)

                if IsDead().check(self.world.player):
                    EventManager.post(NewSceneEvent(game_over(self.world)))
                    return

                EventManager.post(
                    NewSceneEvent(resolution.next_scene(self.world)))
        elif isinstance(event, InputEvent):
            self._handle_input(event)
