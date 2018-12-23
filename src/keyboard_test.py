from unittest.mock import patch, MagicMock
from unittest import TestCase
from keyboard import Keyboard
from typing import Any
from events import Event
from events import InputEvent
import pygame


class KeyboardTest(TestCase):

    @patch('event_manager.EventManager')
    def get_keyboard(self, EventManager: Any) -> None:
        self.keyboard = Keyboard(EventManager())

    def setUp(self) -> None:
        self.get_keyboard()

    def test_quit(self) -> None:
        quit_event = [pygame.event.Event(pygame.QUIT, {'unicode': 'esc'})]
        self.keyboard.get_pygame_events = MagicMock(return_value=quit_event)

        self.keyboard.notify(Event.TICK)

        self.keyboard.event_manager.post.assert_called_once_with(Event.QUIT)

    def test_unbound_key_posts_no_events(self) -> None:
        quit_event = [pygame.event.Event(pygame.KEYDOWN, {'unicode': 'a', 'key': 97})]
        self.keyboard.get_pygame_events = MagicMock(return_value=quit_event)

        self.keyboard.notify(Event.TICK)

        self.keyboard.event_manager.post.never_called()

    def test_bound_key_posts_bound_event(self) -> None:
        self.keyboard.get_binding = MagicMock(return_value=Event.SETTINGS)
        event = [pygame.event.Event(pygame.KEYDOWN, {'unicode': 'x', 'key': 97})]
        self.keyboard.get_pygame_events = MagicMock(return_value=event)

        self.keyboard.notify(Event.TICK)

        self.keyboard.event_manager.post.assert_called_once_with(Event.SETTINGS)

    def test_mouse_click_posts_mouse_event(self) -> None:
        mouse = (460, 680)
        mouse_event = InputEvent(Event.MOUSE_CLICK, mouse=mouse)
        event = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'unicode': '', 'key': 97})]
        self.keyboard.get_pygame_events = MagicMock(return_value=event)
        self.keyboard.mouse_event = MagicMock(return_value=mouse_event)

        self.keyboard.notify(Event.TICK)

        self.keyboard.event_manager.post.assert_called_once_with(mouse_event)
