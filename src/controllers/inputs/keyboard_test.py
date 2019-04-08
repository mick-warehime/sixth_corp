from unittest import TestCase
from unittest.mock import MagicMock

import pygame

from controllers.inputs.keyboard import Keyboard
from events.events_base import EventTypes, EventListener, EventType, InputEvent


class BasicListener(EventListener):

    def __init__(self):
        super().__init__()
        self.events = []

    def notify(self, event: EventType) -> None:
        self.events.append(event)


class KeyboardTest(TestCase):

    def setUp(self) -> None:
        self.keyboard = Keyboard()

    def test_quit(self) -> None:
        listener = BasicListener()
        quit_event = [pygame.event.Event(pygame.QUIT, {'unicode': 'esc'})]
        self.keyboard.get_pygame_events = MagicMock(return_value=quit_event)

        self.keyboard.notify(EventTypes.TICK)

        assert listener.events == [EventTypes.QUIT]

    def test_unbound_key_posts_input_event(self) -> None:
        listener = BasicListener()
        key_val = 'a'
        events = [
            pygame.event.Event(pygame.KEYDOWN, {'unicode': key_val, 'key': 97})]
        self.keyboard.get_pygame_events = MagicMock(return_value=events)

        assert not listener.events
        self.keyboard.notify(EventTypes.TICK)
        assert len(listener.events) == 1
        event = listener.events[0]
        assert isinstance(event, InputEvent)
        assert event.event_type == EventTypes.KEYPRESS
        assert event.key == key_val

    def test_bound_key_posts_bound_event(self) -> None:
        listener = BasicListener()
        self.keyboard.get_binding = MagicMock(return_value=EventTypes.SETTINGS)
        event = [
            pygame.event.Event(pygame.KEYDOWN, {'unicode': 'x', 'key': 97})]
        self.keyboard.get_pygame_events = MagicMock(return_value=event)

        self.keyboard.notify(EventTypes.TICK)

        assert listener.events == [EventTypes.SETTINGS]

    def test_mouse_click_posts_mouse_event(self) -> None:
        listener = BasicListener()
        mouse = (460, 680)
        mouse_event = InputEvent(EventTypes.MOUSE_CLICK, mouse=mouse)
        event = [pygame.event.Event(pygame.MOUSEBUTTONDOWN,
                                    {'unicode': '', 'key': 97})]
        self.keyboard.get_pygame_events = MagicMock(return_value=event)
        self.keyboard.mouse_event = MagicMock(return_value=mouse_event)

        self.keyboard.notify(EventTypes.TICK)

        assert listener.events == [mouse_event]
