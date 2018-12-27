from combat_scene import CombatSceneV2, CombatScene
from combat_scene_model import CombatSceneModel
from combat_scene_view import CombatSceneViewV2, CombatSceneView
from controller import Controller
from events import InputEvent, EventType, Event
from pygame import Surface

from scene_controller import SceneController
from world import World


class CombatSceneControllerV2(SceneController):

    def __init__(self, screen: Surface, world: World,
                 scene: CombatSceneV2) -> None:
        super(CombatSceneControllerV2, self).__init__(screen, world, scene)
        options = {k: v.description for k, v in scene.choices.items()}
        self.view = CombatSceneViewV2(self.screen, world.player, scene.enemy,
                                      options)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self.scene.choices:
            self.scene.make_choice(input_event.key)


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
