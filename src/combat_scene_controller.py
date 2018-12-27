from combat_scene import CombatScene
from combat_scene_view import CombatSceneView
from damage_action import DamageAction
from events import InputEvent
from pygame import Surface

from scene_controller import SceneController
from world import World


class CombatSceneController(SceneController):

    def __init__(self, screen: Surface, world: World,
                 scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__(screen, world, scene)
        self.view = CombatSceneView(self.screen, self.world.player, scene.enemy)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key == '1':
            action = DamageAction(1)
        elif input_event.key == '2':
            action = DamageAction(5)
        else:
            return
        action.apply(self.scene.enemy)
        self._handle_enemy_action()

    def _handle_enemy_action(self) -> None:
        action = DamageAction(1)
        action.apply(self.world.player)
