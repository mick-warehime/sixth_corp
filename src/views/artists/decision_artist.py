from textwrap import wrap
from typing import Callable, List, Union

from data.colors import GREEN
from data.constants import TEXTWIDTH
from models.scenes.decision_scene import DecisionScene
from models.scenes.scenes_base import Scene
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical
from views.artists.scene_artist_base import SceneArtist
from views.layouts import Layout
from views.pygame_screen import Screen

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

    def render(self, screen: Screen, scene: Scene, layout: Layout) -> None:
        assert isinstance(scene, DecisionScene)
        main_text = scene.prompt
        options = {key_val: choice.description
                   for key_val, choice in scene.choices.items()}
        option_text = ['{}: {}'.format(k, v) for k, v in options.items()]
        main_text_fun = _parse_text_fun(main_text)

        texts = _format_text(main_text_fun(), option_text)

        x, font_size, spacing = rescale_horizontal(250, 40, 50)
        y, = rescale_vertical(250)
        screen.render_texts(texts, font_size=font_size, x=x, y=y, color=GREEN,
                            spacing=spacing)
