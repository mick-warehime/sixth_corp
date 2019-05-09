"""Implementation of ViewManager."""
import logging
from typing import Optional

from events.events_base import (BasicEvents, EventListener, EventType,
                                NewSceneEvent)
from views.scene_view import SceneView


class ViewManager(EventListener):
    """Manages the current active view.

    This is a singleton class that switches and updates the current view active
    on the screen.
    """
    current_view: Optional[SceneView] = None

    @classmethod
    def notify(cls, event: EventType) -> None:
        if isinstance(event, NewSceneEvent):
            logging.debug('Updating view to new scene: {}'.format(event.scene))
            cls.current_view = SceneView(event.scene)
        elif event == BasicEvents.TICK:
            assert cls.current_view is not None, ('no scene loaded after '
                                                  'ViewManager initialized.')
            cls.current_view.update()
        elif event == BasicEvents.DEBUG:
            assert cls.current_view is not None, ('no scene loaded after '
                                                  'ViewManager initialized.')
            logging.debug('Toggling debug mode.')
            cls.current_view.toggle_debug()
