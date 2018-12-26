import pygame
from pygame_view import PygameView
from textwrap import wrap
from typing import Dict
from typing import List


def _format_text(description: str,
                 option_texts: List[str]) -> List[str]:
    lines = description.split('\n') + option_texts
    adjusted_lines: List[str] = []
    for line in lines:
        adjusted_lines += wrap(line, DecisionSceneView.WIDTH)
    return adjusted_lines


class DecisionSceneView(PygameView):
    WIDTH = 50

    def __init__(self, screen: pygame.Surface,
                 main_text: str, options: Dict[str, str]) -> None:
        super(DecisionSceneView, self).__init__(screen)

        option_text = ['{}: {}'.format(k, v) for k, v in options.items()]
        self.texts = _format_text(main_text, option_text)

    def render(self) -> None:
        self.render_text()
