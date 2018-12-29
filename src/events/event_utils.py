from events.events_base import Event
from events.events_base import EventManager
from events.events_base import InputEvent
from events.events_base import NewSceneEvent
from scenes.scenes_base import Scene


def simulate_key_press(key_name: str) -> None:
    event = InputEvent(event=Event.KEYPRESS, key=key_name)
    EventManager.post(event)


def post_scene_change(new_scene: Scene) -> None:
    EventManager.post(NewSceneEvent(new_scene))
