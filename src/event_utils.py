from events import Event
from events import EventManager
from events import InputEvent
from events import NewSceneEvent
from scenes_base import Scene


def simulate_key_press(key_name: str) -> None:
    event = InputEvent(event=Event.KEYPRESS, key=key_name)
    EventManager.post(event)


def post_scene_change(new_scene: Scene) -> None:
    EventManager.post(NewSceneEvent(new_scene))
