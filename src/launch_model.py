from event_manager import EventManager
from abstract_model import Model


class LaunchModel(Model):
    def __init__(self, event_manager: EventManager) -> None:
        super(LaunchModel, self).__init__(event_manager)
