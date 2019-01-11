import logging

from characters.character_base import Character
from characters.player import get_player
from controllers.combat_scene_model import CombatSceneModel
from controllers.controller import Controller
from controllers.pygame_collisions import point_collides_rect
from events.events_base import Event, EventType, InputEvent
from scenes.combat_scene import CombatScene
from views.combat_scene_view import CombatSceneView


class CombatSceneController(Controller):

    def __init__(self, scene: CombatScene) -> None:
        super(CombatSceneController, self).__init__()
        self.model = CombatSceneModel(scene)

        self._characters = [get_player(), self.model.enemy()]
        self.selected_character: Character = None

        self.view: CombatSceneView = CombatSceneView()
        self.update()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return
        if isinstance(event, InputEvent):
            self._handle_input(event)
            self.update()

    def _handle_input(self, input_event: InputEvent) -> None:
        if input_event.event == Event.MOUSE_CLICK:
            self._handle_mouse(input_event)
            return

        input_key = int(input_event.key)
        moves = self.model.player_moves(self.selected_character)
        if input_key <= len(moves) and input_key > 0:
            selected_move = moves[input_key - 1]
            self.model.select_player_move(selected_move)

    def _handle_mouse(self, input_event: InputEvent) -> None:
        x = input_event.mouse[0]
        y = input_event.mouse[1]
        for char in self._characters:
            pos = char.position
            if point_collides_rect(x, y, pos.x, pos.y, pos.w, pos.h):
                if self.selected_character == char:
                    continue
                self.selected_character = char
                logging.debug('MOUSE: Selected: {}'.format(char))
                return

        logging.debug('MOUSE: Clicked nothing.')
        # if no character was clicked clear field
        if self.selected_character is not None:
            logging.debug(
                'MOUSE: Deselected: {}'.format(self.selected_character))

        self.selected_character = None

    def update(self) -> None:
        moves = self.model.player_moves(self.selected_character)
        self.view.update(get_player(), self.model.enemy(), moves,
                         self.selected_character)
        self.model.update()
