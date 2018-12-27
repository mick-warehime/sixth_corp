from events import Event
from events import EventManager
from events import InputEvent


def simulate_key_press(key_name: str) -> None:
    event = InputEvent(event=Event.KEYPRESS, key=key_name)
    EventManager.post(event)
