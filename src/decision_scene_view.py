from decision_scene import DecisionOption
import pygame
from pygame_view import PygameView
from textwrap import wrap
from typing import Dict
from typing import List


class DecisionSceneView(PygameView):
    WIDTH = 50

    def __init__(self, screen: pygame.Surface,
                 main_text: str, options: Dict[str, str]) -> None:
        super(DecisionSceneView, self).__init__(screen)

        self.name = main_text
        option_text = self.create_option_text(options)
        self.texts = self.format_text(main_text, option_text)
        print(self.texts)

    def render(self) -> None:
        self.render_text()

    def create_option_text(self,
                           options: Dict[str, str]) -> List[str]:
        texts = []
        for option_key, description in options.items():
            text = '{}: {}'.format(option_key, description)
            texts.append(text)
        return texts

    def format_text(self, description: str,
                    option_texts: List[str]) -> List[str]:
        lines = description.split('\n') + option_texts
        adjusted_lines: List[str] = []
        for line in lines:
            adjusted_lines += wrap(line, DecisionSceneView.WIDTH)
        return adjusted_lines
