from controller import Controller
from combat_scene import CombatScene
from combat_scene_view import CombatSceneView
from damage_action import DamageAction
from events import Event, NewSceneEvent, EventType
from events import InputEvent
from events import EventManager
from pygame import Surface
from world import World


class CombatSceneController(Controller):

    def __init__(self, screen: Surface, world: World,
                 scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__(screen)
        self.world = world
        self.scene = scene
        self.view = CombatSceneView(self.screen)

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.update(self.world.player, self.scene.enemy())
            if self.scene.is_resolved():
                resolution = self.scene.get_resolution()
                for effect in resolution.effects:
                    effect.execute(self.world)

                EventManager.post(
                    NewSceneEvent(resolution.next_scene(self.world)))
        elif isinstance(event, InputEvent):
            self._handle_input(event)

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.key == '1':
            action = DamageAction(1)
        elif input_event.key == '2':
            action = DamageAction(5)
        else:
            return
        enemy = self.scene.enemy()
        action.apply(enemy)
        self._handle_enemy_action()

    def _handle_enemy_action(self) -> None:
        action = DamageAction(1)
        action.apply(self.world.player)
