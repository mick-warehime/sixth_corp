from controllers.controller import Controller
from events.events_base import EventType, InputEvent, BasicEvents, EventManager, \
    InventorySelectionEvent
from models.scenes.inventory_scene import InventoryScene, SlotData


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

        # Handle clicks on mod slots
        clicked_obj = self._scene.layout.object_at(x, y)
        if isinstance(clicked_obj, SlotData):
            EventManager.post(InventorySelectionEvent(clicked_obj.mod))
        else:
            EventManager.post(InventorySelectionEvent(None))
