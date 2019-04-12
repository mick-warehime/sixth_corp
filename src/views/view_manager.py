"""Implementation of ViewManager."""
import logging

from events.events_base import (EventListener, EventType, EventTypes,
                                NewSceneEvent)
from views.scene_view import SceneView


class ViewManager(EventListener):
    """Manages the current active view.

    This is a singleton class that switches and updates the current view active
    on the screen.
    """
    current_view: SceneView = None

    @classmethod
    def notify(cls, event: EventType) -> None:
        if isinstance(event, NewSceneEvent):
            logging.debug('Updating view to new scene: {}'.format(event.scene))
            cls.current_view = SceneView(event.scene)
        elif event == EventTypes.TICK:
            cls.current_view.update()
        elif event == EventTypes.DEBUG:
            logging.debug('Toggling debug mode.')
            cls.current_view.toggle_debug()
