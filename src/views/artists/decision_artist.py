from textwrap import wrap
from typing import Callable, List, Union

from data.colors import GREEN
from data.constants import TEXTWIDTH
from scenes.decision_scene import DecisionScene
from views.scene_artist_base import SceneArtist
from views.screen_base import Screen

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


class DecisionArtist(SceneArtist):

    def render(self, screen: Screen, scene: DecisionScene) -> None:
        main_text = scene.prompt
        options = {key_val: choice.description
                   for key_val, choice in scene.choices.items()}
        option_text = ['{}: {}'.format(k, v) for k, v in options.items()]
        main_text_fun = _parse_text_fun(main_text)

        texts = _format_text(main_text_fun(), option_text)
        screen.render_texts(texts, font_size=40, x=250, y=250, color=GREEN, spacing=50)