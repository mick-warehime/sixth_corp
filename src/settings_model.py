from events import EventManager
from abstract_model import Model


class SettingsModel(Model):
    def __init__(self, event_manager: EventManager) -> None:
        super(SettingsModel, self).__init__(event_manager)
