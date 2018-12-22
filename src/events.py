from typing import Tuple
from enum import Enum


class Event(Enum):
    NONE = 'NONE'
    QUIT = 'QUIT'
    TICK = 'TICK'
    KEYDOWN = 'KEYDOWN'
    KEYUP = 'KEYUP'
    MOUSE_CLICK = 'MOUSE_CLICK'

    # bindable events
    OPEN_SETTINGS = 'OPEN_SETTINGS'
    CLOSE_SETTINGS = 'CLOSE_SETTINGS'

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
        return '%s, key=%s, mouse=%s, pressed=%s' % (self.event, self.key, self.mouse, self.pressed)
