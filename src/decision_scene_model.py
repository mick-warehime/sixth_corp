from events import EventManager
from abstract_model import Model


class DecisionSceneModel(Model):
    def __init__(self, event_manager: EventManager) -> None:
        super(DecisionSceneModel, self).__init__(event_manager)
