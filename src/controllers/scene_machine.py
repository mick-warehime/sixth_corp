from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.inventory_controller import InventoryController
from controllers.settings_controller import SettingsController
from events.events_base import Event, EventListener, EventType, NewSceneEvent
from scenes.combat_scene import CombatScene
from scenes.decision_scene import DecisionScene
from scenes.scene_examples import loading_scene
from scenes.scenes_base import Scene

SCENE_CONTROLLERS = {DecisionScene: DecisionSceneController,
                     CombatScene: CombatSceneController}
INTERUPT_CONTROLLERS = [Event.SETTINGS, Event.INVENTORY]


def interupt_controller(event: EventType) -> Controller:
    if event == Event.SETTINGS:
        return SettingsController()
    elif event == Event.INVENTORY:
        return InventoryController()
    else:
        raise ValueError('No controller set for event {}'.format(event))


class SceneMachine(EventListener):
    """Handles transitions between scenes."""

    def __init__(self) -> None:
        super().__init__()
        self.controller: Controller = None
        self._game_controller: Controller = None
        self._prev_controller: Controller = None
        self._set_next_scene(loading_scene())
        self._interupted = False
        self._interupting_event: EventType = None

    def notify(self, event: EventType) -> None:
        if event in INTERUPT_CONTROLLERS:
            self._toggle_interupt(event)
        if isinstance(event, NewSceneEvent):
            self._set_next_scene(event.scene)

    def _set_next_scene(self, scene: Scene) -> None:
        scene_type = type(scene)
        assert scene_type in SCENE_CONTROLLERS

        controller = SCENE_CONTROLLERS[scene_type]
        self.controller = controller(scene)
        self._game_controller = self.controller

    def _toggle_interupt(self, event: EventType) -> None:
        if not self._interupted or self._interupting_event != event:
            # Game was not interupted or we are going from one interupt to the next.
            self.controller = interupt_controller(event)
            self._prev_controller = self._game_controller
            self._interupted = True
            self._interupting_event = event
        else:
            # Resume gameplay
            temp_ctrl = self.controller
            self.controller = self._game_controller
            self._prev_controller = temp_ctrl
            self._interupted = False
            self._interupting_event = None

        self.controller.activate()
        self._prev_controller.deactivate()
