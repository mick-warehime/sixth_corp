from controllers.controller import Controller
from events.events_base import Event, EventType
from scenes.inventory_scene import InventoryScene
from views.view_factory import SceneViewType, build_scene_view


class InventoryController(Controller):

    def __init__(self) -> None:
        super().__init__()
        self.view = build_scene_view(SceneViewType.Inventory, InventoryScene())
        self.update()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return

        if event != Event.TICK:
            self.update()

    def update(self) -> None:
        self.view.update()
