import logging

from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import (ControllerActivatedEvent, EventType,
                                EventTypes, InputEvent, MoveExecutedEvent)
from models.scenes.combat_scene import CombatScene

COMBAT_KEYBOARD_INPUTS = [str(i) for i in range(9)]


class CombatSceneController(Controller):
    """Controls updates for objects in a Combat Scene."""

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.scene = scene
        self._update_scene()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if isinstance(event, InputEvent):
            self._handle_input(event)
            self._update_scene()
        elif isinstance(event, MoveExecutedEvent):
            self._handle_move_executed(event)
        elif isinstance(event, ControllerActivatedEvent):
            self._update_scene()

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.event_type == EventTypes.MOUSE_CLICK:
            self._handle_mouse_click(input_event)
            return

        if input_event.key in COMBAT_KEYBOARD_INPUTS:
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

        # Check if a character was newly clicked.
        clicked_obj = self.scene.layout.object_at(x, y)
        if clicked_obj in self.scene.characters():
            if self.scene.selected_char != clicked_obj:
                self.scene.selected_char = clicked_obj
                logging.debug('MOUSE: Selected: {}'.format(clicked_obj))
                return

        logging.debug('MOUSE: Clicked nothing.')
        # if no character was clicked clear field
        if self.scene.selected_char is not None:
            logging.debug(
                'MOUSE: Deselected: {}'.format(self.scene.selected_char))
            self.scene.selected_char = None

    def _handle_move_executed(self, event: MoveExecutedEvent) -> None:
        if event.is_attacker_move:
            self.scene.selected_char = None
            self._update_scene()

    def _update_scene(self) -> None:
        self.scene.player_moves(self.scene.selected_char)
        if self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()
            logging.debug('Combat scene resolved.')
            post_scene_change(resolution.next_scene())
