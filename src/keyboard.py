import pygame
from events import Event
from events import InputEvent
from event_listener import EventListener
from event_manager import EventManager
from typing import Tuple, List
from keybindings import Keybindings


class Keyboard(EventListener):
    def __init__(self, event_manager: EventManager) -> None:
        super(Keyboard, self).__init__(event_manager)
        self.bindings = Keybindings()
        self.bindings.load()

    def notify(self, event: Event) -> None:
        if event == Event.TICK:
            self.handle_inputs()

    def handle_inputs(self) -> None:
        # Called for each game tick. We check our keyboard presses here.
        for pg_event in self.get_pygame_events():
            # handle window manager closing our window
            if self.is_quit_event(pg_event):
                self.event_manager.post(Event(Event.QUIT))
            # handle key down events
            elif pg_event.type == pygame.KEYDOWN:
                self.handle_keypress(pg_event.unicode)
            elif pg_event.type == pygame.KEYUP:
                pass
            elif pg_event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()

    def handle_keypress(self, key_name: str) -> None:
        if self.get_binding(key_name) != Event.NONE:
            self.post_bound_event(key=key_name)
        else:
            input_event = InputEvent(event=Event.KEYPRESS, key=key_name)
            self.event_manager.post(input_event)

    def handle_mouse_click(self) -> None:
        mouse_event = self.mouse_event()
        self.event_manager.post(mouse_event)

    def mouse_event(self) -> InputEvent:
        return InputEvent(event=Event.MOUSE_CLICK, key='', mouse=self.mouse_pos())

    def mouse_pos(self) -> Tuple[int, int]:
        return pygame.mouse.get_pos()

    def get_binding(self, key: str) -> Event:
        return self.bindings.get_binding(key)

    def post_bound_event(self, key: str) -> None:
        binding = self.get_binding(key)
        event = self.bindings.event_for_binding(binding)
        return self.event_manager.post(Event(event))

    def get_pygame_events(self) -> List[pygame.event.EventType]:
        return pygame.event.get()

    def is_quit_event(self, pg_event: pygame.event.EventType) -> bool:
        if pg_event.type == pygame.QUIT:
            return True

        return pg_event.type == pygame.KEYDOWN and pg_event.key == pygame.K_ESCAPE
