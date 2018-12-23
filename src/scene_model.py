from event_manager import EventManager
from abstract_model import Model


class SceneModel(Model):
    def __init__(self, event_manager: EventManager) -> None:
        super(SceneModel, self).__init__(event_manager)
