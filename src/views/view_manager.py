"""Implementation of ViewManager."""
import logging

from events.events_base import (EventListener, EventType, BasicEvents,
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
        elif event == BasicEvents.TICK:
            cls.current_view.update()
        elif event == BasicEvents.DEBUG:
            logging.debug('Toggling debug mode.')
            cls.current_view.toggle_debug()
