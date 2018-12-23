from events import Event
import logging
from listener import Listener
from weakref import WeakKeyDictionary


class EventManager(object):
    def __init__(self) -> None:
        self.listeners: WeakKeyDictionary = WeakKeyDictionary()

    def register(self, l: Listener) -> None:
        self.listeners[l] = 1
        logging.debug('registered listener {0} {1}'.format(
            len(self.listeners), l))

    def unregister(self, l: Listener) -> None:
        if l in self.listeners.keys():
            del self.listeners[l]

    def post(self, event: Event) -> None:
        if not event == Event.TICK:
            logging.debug('EVENT: {}'.format(str(event)))

        # use a list to avoid generator changing size during the loop
        for l in list(self.listeners.keys()):
            l.notify(event)
