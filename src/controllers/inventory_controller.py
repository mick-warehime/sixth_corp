from controllers.controller import Controller
from events.events_base import Event, EventType
from models.scenes.inventory_scene import InventoryScene
from views.scene_view import SceneView


class InventoryController(Controller):

    def __init__(self) -> None:
        super().__init__()
        self.view = SceneView(InventoryScene())
        self.update()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return

        if event != Event.TICK:
            self.update()

    def update(self) -> None:
        self.view.update()
