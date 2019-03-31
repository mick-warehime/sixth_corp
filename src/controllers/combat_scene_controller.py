import logging

from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import (ControllerActivatedEvent, Event, EventType,
                                InputEvent, MoveExecutedEvent)
from scenes.combat_scene import CombatScene
from scenes.scene_examples import game_over
from views.scene_view import SceneView

NUMBER_KEYS = [str(i) for i in range(9)]


class CombatSceneController(Controller):
    """Controls updates for objects in a Combat Scene."""

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.scene = scene

        self._view = SceneView(scene)
        self._update_scene_and_view()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if isinstance(event, InputEvent):
            self._handle_input(event)
            self._update_scene_and_view()
        elif isinstance(event, MoveExecutedEvent):
            self._handle_move_executed(event)
        elif isinstance(event, ControllerActivatedEvent):
            self._update_scene_and_view()

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.event == Event.MOUSE_CLICK:
            self._handle_mouse_click(input_event)
            return

        if input_event.key not in NUMBER_KEYS:
            return

        # Player move selection
        input_key = int(input_event.key)
        moves = self.scene.player_moves(self.scene.selected_char)
        if len(moves) >= input_key > 0:
            selected_move = moves[input_key - 1]
            self.scene.select_player_move(selected_move)

    def _handle_mouse_click(self, input_event: InputEvent) -> None:
        x = input_event.mouse[0]
        y = input_event.mouse[1]

        # A single click on an unselected character will select it.
        # Any subsequent clicks will deselect it (and may also select a new
        # character).

        # Check if a character was clicked.
        for char in self.scene.characters():
            if char.rect.collidepoint(x, y):
                if self.scene.selected_char == char:
                    continue
                self.scene.selected_char = char
                logging.debug('MOUSE: Selected: {}'.format(char))
                return

        logging.debug('MOUSE: Clicked nothing.')
        # if no character was clicked clear field
        if self.scene.selected_char is not None:
            logging.debug(
                'MOUSE: Deselected: {}'.format(self.scene.selected_char))
            self.scene.selected_char = None

    def _update_scene_and_view(self) -> None:
        self.scene.player_moves(self.scene.selected_char)
        self._view.update()
        self._update_scene()

    def _handle_move_executed(self, event: MoveExecutedEvent) -> None:
        if event.is_attacker_move:
            self.scene.selected_char = None
            self._update_scene_and_view()

    def _update_scene(self) -> None:
        if self.scene.is_game_over():
            post_scene_change(game_over())
        elif self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()
            logging.debug('Combat scene resolved. Enemy defeated.')
            post_scene_change(resolution.next_scene())
