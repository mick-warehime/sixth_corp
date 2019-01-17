from characters.character_base import Character
from events.events_base import EventListener, EventType, NewSceneEvent

"""Class that represents the current location (sights, sounds, flavors)."""


class Location(EventListener):

    def __init__(self, background_image_path: str) -> None:
        super().__init__()
        self._background_image_path = background_image_path
        self.scene = 0

    @property
    def background_image_path(self) -> str:
        return self._background_image_path

    def random_enemy(self) -> Character:
        raise NotImplemented('Base class must implement random_enemy.')

    def notify(self, event: EventType) -> None:
        if isinstance(event, NewSceneEvent):
            self.scene += 1
