from controller import Controller
from combat_scene import CombatScene
from combat_scene_model import CombatSceneModel
from combat_scene_view import CombatSceneView
from events import Event, EventType
from events import InputEvent
from pygame import Surface

from world import World


class CombatSceneController(Controller):

    def __init__(self, screen: Surface, world: World,
                 scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__(screen)
        self.model = CombatSceneModel(world, scene)
        self.view = CombatSceneView(self.screen)

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.update(self.model.player(), self.model.enemy())
            self.model.update()
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key == '1':
            self.model.damage_enemy(1)
        elif input_event.key == '2':
            self.model.damage_enemy(5)
