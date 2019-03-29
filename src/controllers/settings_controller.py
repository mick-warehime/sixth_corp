from controllers.controller import Controller
from events.events_base import Event, EventType
from scenes.settings_scene import SettingsScene
from views.scene_view import SceneView


class SettingsController(Controller):

    def __init__(self) -> None:
        super(SettingsController, self).__init__()
        self.view = SceneView(SettingsScene())
        self.update()

    def notify(self, event: EventType) -> None:
        if not self._active:
            return

        if event != Event.TICK:
            self.update()

    def update(self) -> None:
        self.view.update()
