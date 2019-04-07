from controllers.combat_scene_controller import CombatSceneController
from controllers.controller import Controller
from controllers.decision_scene_controller import DecisionSceneController
from controllers.inventory_controller import InventoryController
from controllers.settings_controller import SettingsController
from events.events_base import Event, EventListener, EventType, NewSceneEvent
from models.scenes.combat_scene import CombatScene
from models.scenes.decision_scene import DecisionScene
from scenes.scene_examples import loading_scene
from models.scenes.scenes_base import Scene

SCENE_CONTROLLERS = {DecisionScene: DecisionSceneController,
                     CombatScene: CombatSceneController}
INTERUPT_CONTROLLERS = [Event.SETTINGS, Event.INVENTORY]


def interrupt_controller(event: EventType) -> Controller:
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
        self._interrupted = False
        self._interrupting_event: EventType = None

    def notify(self, event: EventType) -> None:
        if event in INTERUPT_CONTROLLERS:
            self._toggle_interrupt(event)
        if isinstance(event, NewSceneEvent):
            self._set_next_scene(event.scene)

    def _set_next_scene(self, scene: Scene) -> None:
        scene_type = type(scene)
        assert scene_type in SCENE_CONTROLLERS

        controller = SCENE_CONTROLLERS[scene_type]
        self.controller = controller(scene)
        self._game_controller = self.controller

    def _toggle_interrupt(self, event: EventType) -> None:
        if not self._interrupted or self._interrupting_event != event:
            # Game was not interrupted or we are going from one interrupt to the
            # next.
            self.controller = interrupt_controller(event)
            self._prev_controller = self._game_controller
            self._interrupted = True
            self._interrupting_event = event
        else:
            # Resume gameplay
            temp_ctrl = self.controller
            self.controller = self._game_controller
            self._prev_controller = temp_ctrl
            self._interrupted = False
            self._interrupting_event = None

        self.controller.activate()
        self._prev_controller.deactivate()
