from controllers.controller import Controller
from events.events_base import EventType, InputEvent, BasicEvents
from models.scenes.inventory_scene import InventoryScene


class InventoryController(Controller):
    """Handles user inputs for the inventory scene"""

    def __init__(self, scene: InventoryScene) -> None:
        super().__init__()
        self._scene = scene

    def _notify(self, event: EventType) -> None:
        if isinstance(event, InputEvent):
            if event.event_type == BasicEvents.MOUSE_CLICK:
                self._handle_mouse_click(event)
                return

    def _handle_mouse_click(self, event: InputEvent):
        x = event.mouse[0]
        y = event.mouse[1]

        clicked_obj = self._scene.layout.object_at(x, y)
        print(str(clicked_obj))
