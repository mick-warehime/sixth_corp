import logging

from controllers.controller import Controller
from events.event_utils import post_scene_change
from events.events_base import (BasicEvents, EventManager, EventType,
                                InputEvent, InventorySelectionEvent,
                                InventoryTransferEvent)
from models.scenes.inventory_scene import InventoryScene, SlotData, SlotHeader


class InventoryController(Controller):
    """Handles user inputs for the inventory scene"""

    def __init__(self, scene: InventoryScene) -> None:
        super().__init__()
        self._scene = scene

    def _notify(self, event: EventType) -> None:
        if isinstance(event, InputEvent):
            if event.event_type == BasicEvents.MOUSE_CLICK:
                self._handle_mouse_click(event)

        if self._scene.is_resolved():
            resolution = self._scene.get_resolution()
            for effect in resolution.effects:
                effect.execute()
            logging.debug('Exiting inventory scene.')
            self.deactivate()
            post_scene_change(resolution.next_scene())

    def _handle_mouse_click(self, event: InputEvent) -> None:
        x = event.mouse[0]
        y = event.mouse[1]

        # Handle clicks on mod slots
        clicked_obj = self._scene.layout.object_at(x, y)
        # Player clicks on a mod.
        if isinstance(clicked_obj, SlotData):
            EventManager.post(InventorySelectionEvent(clicked_obj.mod))
        # Player clicks on a slot category -> attempt mod transfer.
        elif isinstance(clicked_obj, SlotHeader):
            EventManager.post(InventoryTransferEvent(clicked_obj.slot))
            EventManager.post(InventorySelectionEvent(None))
        else:
            EventManager.post(InventorySelectionEvent(None))
