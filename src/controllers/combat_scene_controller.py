from characters.player import get_player
from scenes.combat_scene import CombatScene
from controllers.combat_scene_model import CombatSceneModel, CombatTargeting
from views.combat_scene_view import CombatSceneView
from controllers.controller import Controller
from events.events_base import InputEvent, EventType, Event


class CombatSceneController(Controller):

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.model = CombatSceneModel(scene)
        player = get_player()
        targets = (player, self.model.enemy())
        self._targeting = CombatTargeting(player, targets)
        self.view = CombatSceneView()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.update(get_player(), self.model.enemy(),
                             self._targeting.abilities_available())
            self.model.update()
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def _handle_input(self, input_event: InputEvent) -> None:

        abilities = self._targeting.abilities_available()
        if self._ability_selected(input_event, len(abilities)):
            ability = abilities[int(input_event.key) - 1]
            self._targeting.select_ability(ability)
            self.view.show_targets(self._targeting.valid_targets())
            return

        targets = self._targeting.valid_targets()
        if self._target_selected(input_event, len(targets)):
            ability = self._targeting.selected_ability
            target = targets[int(input_event.key) - 1]
            self.model.apply_player_ability(ability, target)
            self.model.handle_enemy_action()
            self.view.hide_targets()
            return

    def _target_selected(self, input_event, num_targets):
        targeting_keys = [str(k + 1) for k in range(num_targets)]
        return self.view.targets_shown() and input_event.key in targeting_keys

    def _ability_selected(self, input_event, num_abilities):
        ability_keys = [str(k + 1) for k in range(num_abilities)]
        return not self.view.targets_shown() and input_event.key in ability_keys
