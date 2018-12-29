from scenes.combat_scene import CombatScene
from models.combat_scene_model import CombatSceneModel
from views.combat_scene_view import CombatSceneView
from controllers.controller import Controller
from events.events_base import InputEvent, EventType, Event
from models.world import World


class CombatSceneController(Controller):

    def __init__(self, world: World,
                 scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.model = CombatSceneModel(world, scene)
        self.view = CombatSceneView()

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
