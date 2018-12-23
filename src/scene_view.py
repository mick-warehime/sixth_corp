import pygame
from event_manager import EventManager
from pygame_view import PygameView


class SceneView(PygameView):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface, scene_name: str) -> None:
        super(SceneView, self).__init__(event_manager, screen)
        self.name = scene_name
        self.texts = [
            'Hark! Scene {}'.format(scene_name),
            'N: Continue',
            'X: Settings',
            'Esc: Quit']

    def render(self) -> None:
        self.render_text()
