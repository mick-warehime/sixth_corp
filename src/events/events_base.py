import abc
import logging
from enum import Enum
from typing import NamedTuple, Optional, Tuple, Union
from weakref import WeakSet

from models.characters.character_base import Character
from models.characters.mods_base import Mod, SlotTypes
from models.characters.moves_base import Move
from models.scenes.scenes_base import Scene


class BasicEvents(Enum):
    NONE = 'NONE'  # Null event, signifies nothing.
    QUIT = 'QUIT'  # signals to quit the game.
    TICK = 'TICK'  # single tick of the game clock.
    KEYDOWN = 'KEYDOWN'
    KEYUP = 'KEYUP'
    MOUSE_CLICK = 'MOUSE_CLICK'
    KEYPRESS = 'KEYPRESS'
    DEBUG = 'DEBUG'  # Toggle debug mode

    # bindable events
    SETTINGS = 'SETTINGS'
    INVENTORY = 'INVENTORY'

    # comparing enums gives wrong result without this
    # has to do with this file being imported twice
    # but i can't for the life of me figure out why/how/where
    def __eq__(self, other: object) -> bool:
        if isinstance(other, BasicEvents):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return self.value


class NewSceneEvent(object):

    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def __str__(self) -> str:
        return 'NewSceneEvent({})'.format(str(self.scene))


class InputEvent(NamedTuple):
    event_type: BasicEvents
    key: str = ''
    pressed: bool = False
    mouse: Tuple[int, int] = (-1, -1)

    def __str__(self) -> str:
        return '%s, key=%s, mouse=%s, pressed=%s' % (
            self.event_type, self.key, self.mouse, self.pressed)


class MoveExecutedEvent(NamedTuple):
    """This event is triggered when any character executes a move."""
    move: Move
    is_attacker_move: bool

    def __str__(self) -> str:
        team_str = 'ATTACK MOVE' if self.is_attacker_move else 'DEFEND MOVE'
        return '%s - %s' % (team_str, self.move.description())


class ControllerActivatedEvent(NamedTuple):
    """This event is triggered when a controller is activated or deactivated."""
    status: str

    def __str__(self) -> str:
        return '{}'.format(self.status)


class SelectCharacterEvent(NamedTuple):
    character: Optional[Character]


class SelectPlayerMoveEvent(NamedTuple):
    move: Move

    def __str__(self) -> str:
        return 'SelectPlayerMove({})'.format(self.move)


class DecisionEvent(NamedTuple):
    choice: str
    # We included a scene reference in case two DecisionScenes are listening.
    scene: Scene


class InventorySelectionEvent(NamedTuple):
    mod: Optional[Mod]


class InventoryTransferEvent(NamedTuple):
    new_slot: SlotTypes


EventType = Union[BasicEvents, InputEvent, NewSceneEvent, MoveExecutedEvent,
                  ControllerActivatedEvent, SelectCharacterEvent,
                  SelectPlayerMoveEvent, DecisionEvent, InventorySelectionEvent,
                  InventoryTransferEvent]


class EventManager(object):
    listeners: WeakSet = WeakSet()

    @classmethod
    def register(cls, l: 'EventListener') -> None:
        cls.listeners.add(l)
        logging.debug('registered listener {0} {1}'.format(
            len(cls.listeners), l))

    @classmethod
    def post(cls, event: EventType) -> None:
        if not event == BasicEvents.TICK:
            logging.debug('EVENT: {}'.format(str(event)))

        for l in cls.listeners.copy():
            l.notify(event)


class EventListener(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        EventManager.register(self)

    @abc.abstractmethod
    def notify(self, event: EventType) -> None:
        """Notify the listener of an event."""
        pass
