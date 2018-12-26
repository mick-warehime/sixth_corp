from controller import Controller
from events import Event
from settings_view import SettingsView
from pygame import Surface


class SettingsController(Controller):

    def __init__(self, screen: Surface) -> None:
        super(SettingsController, self).__init__(screen)
        self.view = SettingsView(self.screen)

    def notify(self, event: Event) -> None:
        if not self._active:
            return
        if event == Event.TICK:
            self.view.render()
