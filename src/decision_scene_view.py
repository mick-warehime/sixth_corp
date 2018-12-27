import pygame
from constants import TEXTWIDTH
from pygame_view import PygameView
from textwrap import wrap
from typing import Dict, Callable, Union
from typing import List

_TextFun = Callable[[], str]
_TextOrFun = Union[str, _TextFun]


def _format_text(main_text: str,
                 option_texts: List[str]) -> List[str]:
    lines = main_text.split('\n') + option_texts
    adjusted_lines: List[str] = []
    for line in lines:
        adjusted_lines += wrap(line, TEXTWIDTH)
    return adjusted_lines


def _parse_text_fun(main_text: _TextOrFun) -> _TextFun:
    if isinstance(main_text, str):
        def text_fun() -> str:
            return main_text  # type:ignore
    else:
        text_fun = main_text  # type:ignore

    return text_fun


class DecisionSceneView(PygameView):

    def __init__(self, screen: pygame.Surface,
                 main_text: _TextOrFun, options: Dict[str, str]) -> None:
        super(DecisionSceneView, self).__init__(screen)

        self._option_text = ['{}: {}'.format(k, v) for k, v in options.items()]
        self._main_text_fun = _parse_text_fun(main_text)
        self.texts = _format_text(self._main_text_fun(), self._option_text)

    def render(self) -> None:
        self.texts = _format_text(self._main_text_fun(), self._option_text)
        self.render_text()
