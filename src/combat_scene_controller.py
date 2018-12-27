from combat_scene import CombatScene
from combat_scene_view import CombatSceneView
from decision_scene_view import DecisionSceneView
from events import InputEvent
from pygame import Surface

from scene_controller import SceneController
from world import World


class CombatSceneController(SceneController):

    def __init__(self, screen: Surface, world: World,
                 scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__(screen, world, scene)
        options = {k: v.description for k, v in scene.choices.items()}
        self.view = CombatSceneView(self.screen, world.player, scene.enemy,
                                    options)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self.scene.choices:
            self.scene.make_choice(input_event.key)
