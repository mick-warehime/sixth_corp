from models.player import get_player
from scenes.combat_scene import CombatScene
from models.combat_scene_model import CombatSceneModel
from views.combat_scene_view import CombatSceneView
from controllers.controller import Controller
from events.events_base import InputEvent, EventType, Event


class CombatSceneController(Controller):

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.model = CombatSceneModel(scene)
        self.view = CombatSceneView()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.update(get_player(), self.model.enemy(),
                             self.model.usable_abilities())
            self.model.update()
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def _handle_input(self, input_event: InputEvent) -> None:
        ability_keys = [str(k + 1) for k in
                        range(len(self.model.usable_abilities()))]
        targeting_keys = [str(k + 1) for k in
                          range(len(self.model.valid_targets()))]

        if self._ability_selected(ability_keys, input_event):
            self.model.select_ability(int(input_event.key) - 1)
            self.view.enable_targetting(self.model.valid_targets())

        elif self._target_selected(input_event, targeting_keys):
            self.view.disable_targetting()
            self.model.apply_player_ability(int(input_event.key) - 1)
            self.model._handle_enemy_action()

    def _target_selected(self, input_event, targeting_keys):
        return (self.view.targetting_enabled
                and input_event.key in targeting_keys)

    def _ability_selected(self, ability_keys, input_event):
        return (not self.view.targetting_enabled
                and input_event.key in ability_keys)
