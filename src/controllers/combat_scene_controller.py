import logging

from characters.player import get_player
from controllers.controller import Controller
from controllers.pygame_collisions import point_collides_rect
from events.event_utils import post_scene_change
from events.events_base import (ControllerActivatedEvent, Event, EventType,
                                InputEvent, MoveExecutedEvent)
from scenes.combat_scene import CombatScene
from scenes.scene_examples import game_over
from views.stack_utils import point_collides_stack_element
from views.view_factory import SceneViewType, build_scene_view

NUMBER_KEYS = [str(i) for i in range(9)]


class CombatSceneController(Controller):

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.scene = scene

        self._characters = [get_player(), self.scene.enemy()]

        self.view = build_scene_view(SceneViewType.Combat, scene)
        self.update()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if isinstance(event, InputEvent):
            self._handle_input(event)
            self.update()
        elif isinstance(event, MoveExecutedEvent):
            self._handle_move_executed(event)
        elif isinstance(event, ControllerActivatedEvent):
            self.update()

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.event == Event.MOUSE_CLICK:
            self._handle_mouse(input_event)
            return

        if input_event.key not in NUMBER_KEYS:
            return

        input_key = int(input_event.key)
        moves = self.scene.player_moves()
        if len(moves) >= input_key > 0:
            selected_move = moves[input_key - 1]
            self.scene.select_player_move(selected_move)
            self.scene.append_stack(selected_move)

    def _handle_mouse(self, input_event: InputEvent) -> None:
        x = input_event.mouse[0]
        y = input_event.mouse[1]
        self._handle_character_selection(x, y)
        self._handle_stack_selection(x, y)

    def _handle_stack_selection(self, x: int, y: int) -> None:
        for i in range(len(self.scene.stack)):
            if point_collides_stack_element(i, x, y):
                self.scene.try_pop_stack(i)
                break
        logging.debug('MOUSE: Clicked nothing.')

    def _handle_character_selection(self, x: int, y: int) -> None:
        for char in self._characters:
            pos = char.position
            if point_collides_rect(x, y, pos.x, pos.y, pos.w, pos.h):
                if self.scene.selected == char:
                    continue
                self.scene.selected = char
                logging.debug('MOUSE: Selected: {}'.format(char))
                return

        logging.debug('MOUSE: Clicked nothing.')
        # if no character was clicked clear field
        if self.scene.selected is not None:
            logging.debug(
                'MOUSE: Deselected: {}'.format(self.scene.selected))

            self.scene.selected = None

    def update(self) -> None:
        self.scene.player_moves()
        self.view.update()
        self._update_scene()

    def _handle_move_executed(self, event: MoveExecutedEvent) -> None:
        if event.attacker:
            self.update()

    def _update_scene(self) -> None:
        if self.scene.is_game_over():
            post_scene_change(game_over())
        elif self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()
            logging.debug('Combat scene resolved. Enemy defeated.')
            post_scene_change(resolution.next_scene())
