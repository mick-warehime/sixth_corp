import logging

from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import (BasicEvents, EventManager, EventType,
                                InputEvent, MoveExecutedEvent,
                                SelectCharacterEvent, SelectPlayerMoveEvent)
from models.scenes.combat_scene import CombatScene

COMBAT_KEYBOARD_INPUTS = [str(i) for i in range(9)]


class CombatSceneController(Controller):
    """Processes player input in a Combat Scene."""

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.scene = scene

    def _notify(self, event: EventType) -> None:

        # Do not handle inputs while animation is in progress
        if self.scene.animation_progress is not None:
            return

        if isinstance(event, InputEvent):
            self._handle_input(event)
            self._check_for_resolution()
        elif isinstance(event, MoveExecutedEvent):
            if event.is_attacker_move:
                EventManager.post(SelectCharacterEvent(None))
            self._check_for_resolution()

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.event_type == BasicEvents.MOUSE_CLICK:
            self._handle_mouse_click(input_event)
            return

        if input_event.key in COMBAT_KEYBOARD_INPUTS:
            # Player move selection
            input_key = int(input_event.key)
            moves = self.scene.available_moves()
            if len(moves) >= input_key > 0:
                selected_move = moves[input_key - 1]
                EventManager.post(SelectPlayerMoveEvent(selected_move))

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
                EventManager.post(SelectCharacterEvent(clicked_obj))
                logging.debug('MOUSE: Selected: {}'.format(clicked_obj))
                return

        logging.debug('MOUSE: Clicked nothing.')
        # if no character was clicked clear field
        if self.scene.selected_char is not None:
            logging.debug(
                'MOUSE: Deselected: {}'.format(self.scene.selected_char))
            EventManager.post(SelectCharacterEvent(None))

    def _check_for_resolution(self) -> None:
        if self.scene.is_resolved():
            resolution = self.scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()
            logging.debug('Combat scene resolved.')
            self.deactivate()
            post_scene_change(resolution.next_scene())
