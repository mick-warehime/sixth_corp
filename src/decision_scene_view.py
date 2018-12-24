from decision_scene_option import DecisionOption
from events import EventManager
import pygame
from pygame_view import PygameView
from typing import Dict
from typing import List


class DecisionSceneView(PygameView):
    def __init__(self, event_manager: EventManager, screen: pygame.Surface,
                 main_text: str, options: Dict[str, DecisionOption]) -> None:
        super(DecisionSceneView, self).__init__(event_manager, screen)
        self.name = main_text
        self.texts = [main_text] + self.create_text(options)

    def render(self) -> None:
        self.render_text()

    def create_text(self, options: Dict[str, DecisionOption]) -> List[str]:
        texts = []
        for option_name in options:
            option = options[option_name]
            text = '{}: {}'.format(option_name, option.name)
            texts.append(text)
        return texts
