import logging
from _weakrefset import WeakSet
from enum import Enum
from typing import Tuple


class Event(Enum):
    NONE = 'NONE'
    QUIT = 'QUIT'
    TICK = 'TICK'
    KEYDOWN = 'KEYDOWN'
    KEYUP = 'KEYUP'
    MOUSE_CLICK = 'MOUSE_CLICK'
    KEYPRESS = 'KEYPRESS'

    NEW_SCENE = 'NEW_SCENE'

    # bindable events
    SETTINGS = 'SETTINGS'

    # comparing enums gives wrong result without this
    # has to do with this file being imported twice
    # but i can't for the life of me figure out why/how/where
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Enum):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return self.value


class InputEvent(object):

    def __init__(self, event: Event, key: str = '', pressed: bool = False,
                 mouse: Tuple[int, int] = (-1, -1)) -> None:
        self.event = event
        self.key = key
        self.mouse = mouse
        self.pressed = pressed

    def __str__(self) -> str:
        return '%s, key=%s, mouse=%s, pressed=%s' % (
            self.event, self.key, self.mouse, self.pressed)


class EventManager(object):
    listeners: WeakSet = WeakSet()

    def register(self, l: 'EventListener') -> None:
        self.listeners.add(l)
        logging.debug('registered listener {0} {1}'.format(
            len(self.listeners), l))

    def unregister(self, l: 'EventListener') -> None:
        if l in self.listeners:
            logging.debug('unregistered listener {0} {1}'.format(
                len(self.listeners), l))
            self.listeners.remove(l)

    def post(self, event: Event) -> None:
        if not event == Event.TICK:
            logging.debug('EVENT: {}'.format(str(event)))

        for l in self.listeners.copy():
            l.notify(event)


class EventListener(object):

    def __init__(self, event_manager: EventManager) -> None:
        event_manager.register(self)
        self.event_manager = event_manager

    def notify(self, event: Event) -> None:
        raise NotImplementedError('Subclesses must implement this method.')

    def unregister(self) -> None:
        self.event_manager.unregister(self)
