from events.events_base import (BasicEvents, EventManager, InputEvent,
                                NewSceneEvent)
from models.scenes.scenes_base import Scene


def simulate_mouse_click(x: int, y: int) -> None:
    event = InputEvent(event_type=BasicEvents.MOUSE_CLICK, key='', mouse=(x, y))
    EventManager.post(event)


def simulate_key_press(key_name: str) -> None:
    event = InputEvent(event_type=BasicEvents.KEYPRESS, key=key_name)
    EventManager.post(event)


def post_scene_change(new_scene: Scene) -> None:
    EventManager.post(NewSceneEvent(new_scene))
