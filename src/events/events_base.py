import logging
from enum import Enum
from typing import Tuple, Union
from weakref import WeakSet

from combat.moves_base import Move
from scenes.scenes_base import Scene


class Event(Enum):
    NONE = 'NONE'
    QUIT = 'QUIT'
    TICK = 'TICK'
    KEYDOWN = 'KEYDOWN'
    KEYUP = 'KEYUP'
    MOUSE_CLICK = 'MOUSE_CLICK'
    KEYPRESS = 'KEYPRESS'

    # bindable events
    SETTINGS = 'SETTINGS'
    INVENTORY = 'INVENTORY'

    # comparing enums gives wrong result without this
    # has to do with this file being imported twice
    # but i can't for the life of me figure out why/how/where
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Enum):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return self.value


class NewSceneEvent(object):

    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def __str__(self) -> str:
        return 'NewSceneEvent({})'.format(str(self.scene))


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


class MoveExecutedEvent(object):
    """This event is triggered when any character executes a move."""

    def __init__(self, move: Move, attacker: bool) -> None:
        self.attacker = attacker
        self.move = move

    def __str__(self) -> str:
        team_str = 'ATTACK MOVE' if self.attacker else 'DEFEND MOVE'
        return '%s - %s' % (team_str, self.move.describe())


class ControllerActivatedEvent(object):
    """This event is triggered when a controller is activated or deactivated."""

    def __init__(self, acivation_status: str) -> None:
        self.status = acivation_status

    def __str__(self) -> str:
        return '{}'.format(self.status)


EventType = Union[Event, InputEvent, NewSceneEvent, MoveExecutedEvent, ControllerActivatedEvent]


class EventManager(object):
    listeners: WeakSet = WeakSet()

    @classmethod
    def register(cls, l: 'EventListener') -> None:
        cls.listeners.add(l)
        logging.debug('registered listener {0} {1}'.format(
            len(cls.listeners), l))

    @classmethod
    def post(cls, event: EventType) -> None:
        if not event == Event.TICK:
            logging.debug('EVENT: {}'.format(str(event)))

        for l in cls.listeners.copy():
            l.notify(event)


class EventListener(object):

    def __init__(self) -> None:
        EventManager.register(self)

    def notify(self, event: EventType) -> None:
        raise NotImplementedError('Subclesses must implement this method.')
