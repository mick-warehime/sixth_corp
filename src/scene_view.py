import pygame
from event_manager import EventManager
from pygame_view import PygameView


class SceneView(PygameView):
    def __init__(self, event_manager: EventManager,
                 screen: pygame.Surface, scene_name: str) -> None:
        super(SceneView, self).__init__(event_manager, screen)
        self.name = scene_name

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        scene_text = 'Scene: {}'.format(self.name)
        somewords = self.smallfont.render(scene_text, True, (0, 255, 255))
        self.screen.blit(somewords, (350, 250))
        pygame.display.flip()
