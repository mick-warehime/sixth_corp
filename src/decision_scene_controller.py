from decision_scene import DecisionScene
from decision_scene_view import DecisionSceneView
from events import InputEvent
from pygame import Surface

from scene_controller import SceneController
from world import World


class DecisionSceneController(SceneController):

    def __init__(self, screen: Surface, world: World,
                 scene: DecisionScene) -> None:
        super(DecisionSceneController, self).__init__(screen, world, scene)
        options = {key_val: choice.description
                   for key_val, choice in scene.choices.items()}
        self.view = DecisionSceneView(self.screen, scene.prompt, options)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key in self.scene.choices:
            self.scene.make_choice(input_event.key)
