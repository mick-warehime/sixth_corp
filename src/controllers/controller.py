from events.events_base import (ControllerActivatedEvent, EventListener,
                                EventManager, EventType)


class Controller(EventListener):

    def __init__(self) -> None:
        super(Controller, self).__init__()
        self._active = True

    def activate(self) -> None:
        status = 'Activating a {}'.format(self.__class__.__name__)
        self._active = True
        EventManager.post(ControllerActivatedEvent(status))

    def deactivate(self) -> None:
        status = 'Deactivating a {}'.format(self.__class__.__name__)
        self._active = False
        EventManager.post(ControllerActivatedEvent(status))

    def notify(self, event: EventType) -> None:
        raise NotImplementedError
