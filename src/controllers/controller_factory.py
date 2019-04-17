from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.inventory_controller import InventoryController
from controllers.settings_controller import SettingsController
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene

_KNOWN_SCENES = (DecisionScene, CombatScene, SettingsScene, InventoryScene)


def build_controller(scene: Scene) -> Controller:
    if isinstance(scene, DecisionScene):
        return DecisionSceneController(scene)
    elif isinstance(scene, CombatScene):
        return CombatSceneController(scene)
    elif isinstance(scene, SettingsScene):
        return SettingsController()
    elif isinstance(scene, InventoryScene):
        return InventoryController(scene)
    raise NotImplementedError('Unrecognized scene type {}'.format(type(scene)))
