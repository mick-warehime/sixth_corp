from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.controller_factory import build_controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.inventory_controller import InventoryController
from controllers.settings_controller import SettingsController
from events.event_utils import post_scene_change
from events.events_base import EventTypes, EventListener, EventType, \
    NewSceneEvent
from models.scenes.inventory_scene import InventoryScene
from models.scenes.scenes_base import Scene
from models.scenes.settings_scene import SettingsScene

_TEMPORARY_SCENES = (SettingsScene, InventoryScene)


def interrupt_controller(event: EventType) -> Controller:
    if event == EventTypes.SETTINGS:
        return SettingsController()
    elif event == EventTypes.INVENTORY:
        return InventoryController()
    else:
        raise ValueError('No controller set for event {}'.format(event))


def _event_matches_scene(event: EventTypes, scene: Scene):
    if event == EventTypes.SETTINGS and isinstance(scene, SettingsScene):
        return True
    if event == EventTypes.INVENTORY and isinstance(scene, InventoryScene):
        return True
    return False


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self) -> None:
        super().__init__()
        self._current_controller: Controller = None

        self._current_game_scene: Scene = None  # not inventory or settings.
        self._current_scene: Scene = None

    def notify(self, event: EventType) -> None:

        # toggle between settings/inventory scene and game scene
        if event in (EventTypes.SETTINGS, EventTypes.INVENTORY):
            new_scene: Scene = None
            # go to temp scene
            if self._current_scene is self._current_game_scene:
                if event == EventTypes.SETTINGS:
                    new_scene = SettingsScene()
                else:
                    new_scene = InventoryScene()
            # go back to game scene
            elif _event_matches_scene(event, self._current_scene):
                new_scene = self._current_game_scene

            if new_scene is not None:
                post_scene_change(new_scene)

        # Update scene and current controller
        if isinstance(event, NewSceneEvent):

            if not isinstance(event.scene, (SettingsScene, InventoryScene)):
                self._current_game_scene = event.scene
            self._current_scene = event.scene

            if self._current_controller is not None:
                self._current_controller.deactivate()
            self._current_controller = build_controller(event.scene)
            self._current_controller.activate()

    @property
    def controller(self) -> Controller:
        return self._current_controller
